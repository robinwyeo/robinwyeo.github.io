#!/usr/bin/env python3
"""AviList notebook → Jekyll-friendly Markdown.

The analysis notebooks and phylogeny cache live in a separate clone of the
``ebird-avilist`` repository. This script runs from **robinwyeo.github.io** and
writes ``_data_science/<stem>.md`` (see ``MD`` below) plus static assets under ``assets/`` and
``images/``.

Workflow
--------
1. Run ``jupyter nbconvert --to markdown`` on the AviList notebook.
2. Fix MathJax / Kramdown escaping in prose sections.
3. Find code cells tagged ``phylo-order-tree`` and ``phylo-family-tree`` in the
   resulting markdown and replace their code-fence blocks with the corresponding
   Phylocanvas.gl HTML embeds (loaded from the pre-built .nwk + .json cache).
4. Copy the Newick + JSON cache files to ``assets/data-science/avilist/phylogeny/``
   so the JS loader can ``fetch()`` them if needed (currently the data is inlined).
4½. Wrap every **bare** nbconvert `` ```python `` cell in
   ``<details markdown="1" class="avilist-setup-code">`` (same pattern as setup
   cells) so re-exports keep code collapsed without hand-editing the Markdown.
5. Build YAML front matter from the **first markdown cell** of the notebook
   (page ``#`` title, ``## Date: YYYY-MM-DD``, and a ``tags:`` / ``- tag`` list),
   plus fixed ``permalink`` and ``header.teaser``. Place the title
   ``![...](...)`` **after front matter but before** ``{% raw %}`` so the
   ``/data-science/`` index excerpt is an ``<img>``.
6. Write out the final ``.md`` file for Jekyll.

After each full run, nbconvert images are copied from ``{MD.stem}_files/`` into
``images/data-science/avilist/``; any older ``YYYY-MM-DD-ebird-avilist_*.png``
files from a previous post filename are removed so duplicates do not accumulate.

AviList repo path
-----------------
Default: sibling directory ``../ebird-avilist`` next to this website repo.
Override with env ``EBIRD_AVILIST_ROOT`` (absolute path to the clone root).

Paths inside **ebird-avilist** (as of 2025–2026): notebook
``notebooks/avilist_birds_explore.ipynb``, phylogeny cache under
``data/phylogeny/``, and ``phylo`` module under ``python/``.

Usage
-----
    cd /path/to/robinwyeo.github.io
    python scripts/nbconvert_avilist_postprocess.py           # full run
    python scripts/nbconvert_avilist_postprocess.py md-only   # patch existing .md
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parent.parent
AVILIST_ROOT = Path(
    os.environ.get("EBIRD_AVILIST_ROOT", REPO.parent / "ebird-avilist")
).resolve()
NB = AVILIST_ROOT / "notebooks" / "avilist_birds_explore.ipynb"
# Filename ``YYYY-MM-DD-*.md`` sets Jekyll's collection document date on GitHub Pages;
# ``permalink`` controls the public URL. nbconvert writes ``{stem}.md`` and ``{stem}_files/``.
MD = REPO / "_data_science" / "2026-05-12-ebird-avilist.md"
NB_FILES = REPO / "_data_science" / f"{MD.stem}_files"
PHY_DIR = AVILIST_ROOT / "data" / "phylogeny"

# Fallbacks if the first markdown cell omits a field (ISO date only).
_DEFAULT_TITLE = "Exploring bird diversity with AviList"
_DEFAULT_DATE = "2026-05-12"
_DEFAULT_TAGS = ["AviList", "birds", "taxonomy", "conservation"]
_PERMALINK = "/data-science/ebird-avilist/"

_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# nbconvert writes ``{notebook_output_stem}_{cell}_{output}.png`` into ``{stem}_files/``.
# When ``MD`` is renamed (new date prefix), old ``YYYY-MM-DD-ebird-avilist_*.png`` files
# would otherwise accumulate next to the new ones — prune after each sync.
_AVILIST_NBCONVERT_PNG_RE = re.compile(
    r"^(?P<doc_stem>\d{4}-\d{2}-\d{2}-ebird-avilist)_\d+_\d+\.png$"
)
_LEGACY_NBCONVERT_PNG_RE = re.compile(r"^ebird-avilist_\d+_\d+\.png$")

ASSET_DIR  = REPO / "assets" / "data-science" / "avilist" / "phylogeny"
FIGURE_DIR = REPO / "assets" / "data-science" / "avilist" / "figures"
IMG_DIR    = REPO / "images" / "data-science" / "avilist"

# Listing page excerpt uses the first markdown block after front matter, not
# ``header.teaser``. The title figure must sit *outside* ``{% raw %}`` (before
# the in-post H1) so the archive shows the image.
TEASER_IMAGE_URL = "/images/data-science/avilist/title.png"

# Public URL bases used by the fetch()-based embeds at runtime.
_PHYLO_ASSET_URL_BASE   = "/assets/data-science/avilist/phylogeny"
_FIGURE_ASSET_URL_BASE  = "/assets/data-science/avilist/figures"

# The post-process script lives in scripts/, which is sibling to the repo root.
sys.path.insert(0, str(REPO / "scripts"))
from _nbconvert_shared import (
    cells_with_tag,
    cell_to_str,
    dedent_nbconvert_table_output,
    process_outside_code_fences,
    run_nbconvert,
)

# AviList package (phylo.py) lives in the ebird-avilist repo clone.
sys.path.insert(0, str(AVILIST_ROOT / "python"))
from phylo import phylocanvas_html

# ---------------------------------------------------------------------------
# Helpers: Jekyll front matter from the notebook lead cell
# ---------------------------------------------------------------------------


def _yaml_double_quoted(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _yaml_tag_entry(tag: str) -> str:
    tag = str(tag).strip()
    if _ISO_DATE_RE.match(tag) or re.fullmatch(r"[\w.-]+", tag):
        return f"  - {tag}"
    return f"  - {_yaml_double_quoted(tag)}"


def _parse_lead_markdown_metadata(nb: dict) -> dict[str, object]:
    """Parse ``title``, ``date`` (YYYY-MM-DD), and ``tags`` from the first markdown cell."""
    first_md = ""
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            first_md = cell_to_str(cell)
            break
    out: dict[str, object] = {}
    if not first_md.strip():
        return out

    lines = first_md.splitlines()
    for line in lines:
        s = line.strip()
        m = re.match(r"^#\s+(.+)$", s)
        if m and not s.startswith("##"):
            out["title"] = m.group(1).strip()
            break

    for line in lines:
        m = re.match(r"^##\s+Date:\s*(.+?)\s*$", line.strip(), flags=re.I)
        if not m:
            continue
        cand = m.group(1).strip()
        if _ISO_DATE_RE.match(cand):
            out["date"] = cand
        else:
            print(
                f"[avilist] WARN: lead-cell Date must be ISO YYYY-MM-DD; "
                f"got {cand!r} — using default date"
            )
        break

    tag_list: list[str] = []
    for i, line in enumerate(lines):
        if line.strip() != "tags:" and not line.strip().startswith("tags:"):
            continue
        j = i + 1
        while j < len(lines):
            bare = lines[j].strip()
            if not bare:
                j += 1
                continue
            mt = re.match(r"^-\s+(.+)$", bare)
            if mt:
                tag_list.append(mt.group(1).strip().strip("'\""))
                j += 1
                continue
            break
        break
    if tag_list:
        out["tags"] = tag_list

    return out


def _format_front_matter_inner(meta: dict[str, object]) -> str:
    title = str(meta.get("title") or _DEFAULT_TITLE)
    date = str(meta.get("date") or _DEFAULT_DATE)
    tags_obj = meta.get("tags")
    tags = tags_obj if isinstance(tags_obj, list) and tags_obj else list(_DEFAULT_TAGS)

    parts = [
        f"title: {_yaml_double_quoted(title)}",
        f"date: {date}",
        "tags:",
    ]
    for t in tags:
        parts.append(_yaml_tag_entry(str(t)))
    parts.extend(
        [
            f"permalink: {_PERMALINK}",
            "header:",
            f"  teaser: {TEASER_IMAGE_URL}",
        ]
    )
    return "\n".join(parts)


_LEAD_META_BLOCK_RE = re.compile(
    r'(^|\n)'
    r'(?P<title>\#\s+[^\n]+\n)'
    r'(?P<date>\#\#\s+Date:\s*[^\n]+\n)?'
    r'(?P<tags>tags:\s*\n(?:[ \t]+-[^\n]+\n)+)?',
    flags=re.IGNORECASE,
)


def _strip_lead_cell_meta_from_body(raw: str) -> str:
    """Remove the ``## Date: …`` and ``tags:`` markup from the body markdown.

    Those lines are authored in the notebook lead markdown cell so the post
    metadata travels with the source, but they're already extracted into the
    Jekyll YAML front matter by :func:`_apply_notebook_front_matter` — leaving
    them in the body causes them to render as a stray H2 + bullet list above
    the post intro. This pass strips them when they sit immediately under the
    lead H1, leaving the title heading itself untouched (the layout also prints
    ``page.title``; use :func:`_strip_duplicate_page_title_heading_in_raw` to
    drop that duplicate H1 when needed).
    """

    def _repl(m: re.Match) -> str:
        return m.group(1) + m.group("title")

    return _LEAD_META_BLOCK_RE.sub(_repl, raw, count=1)


def _apply_notebook_front_matter(raw: str) -> str:
    """Replace or prepend Jekyll YAML from the AviList notebook lead markdown cell."""
    nb = _load_nb()
    meta = _parse_lead_markdown_metadata(nb)
    inner = _format_front_matter_inner(meta)
    title = str(meta.get("title") or _DEFAULT_TITLE)
    date = str(meta.get("date") or _DEFAULT_DATE)
    tags_obj = meta.get("tags")
    tags_eff = tags_obj if isinstance(tags_obj, list) and tags_obj else list(_DEFAULT_TAGS)
    ntags = len(tags_eff)
    print(
        f"[avilist] YAML from notebook lead cell: date={date!r}, "
        f"{ntags} tag(s), title={title[:60]!r}{'…' if len(title) > 60 else ''}"
    )
    block = f"---\n{inner}\n---\n"

    if not raw.lstrip().startswith("---"):
        return block + raw

    stripped = raw.lstrip()
    lead_ws = raw[: len(raw) - len(stripped)]
    try:
        end = stripped.index("\n---\n", 3)
    except ValueError:
        return block + raw
    rest = stripped[end + 5 :]
    return lead_ws + block + rest


# ---------------------------------------------------------------------------
# Helpers: notebook cell inspection
# ---------------------------------------------------------------------------

def _load_nb() -> dict:
    return json.loads(NB.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Helpers: build Phylocanvas.gl embed HTML for one tree
# ---------------------------------------------------------------------------


def _build_phylocanvas_embed(
    nwk_file: Path,
    meta_file: Path,
    container_id: str,
    height: int,
    tree_type: str,
    fallback_img: Path | None = None,
    *,
    drilldown: bool = False,
    subtrees_url_base: str | None = None,
    # Asset URL base for the external-data fetch() mode (S1).
    # When set, Newick + meta are fetched at browser runtime rather than inlined.
    asset_url_base: str | None = _PHYLO_ASSET_URL_BASE,
) -> str:
    """Return a self-contained HTML block for one Phylocanvas.gl tree (Jekyll).

    With *asset_url_base* set (the default), the emitted ``<script>`` fetches
    the Newick and meta JSON at render time instead of inlining them.  This
    keeps the Jekyll post small enough for the GitHub Pages build to succeed.
    """
    # Always load meta in Python (needed for legend, FAMILY_SEARCH_ROWS, etc.).
    meta = json.loads(meta_file.read_text(encoding="utf-8"))

    # Derive public fetch() URLs from the asset_url_base.
    if asset_url_base:
        external_nwk_url  = f"{asset_url_base}/{nwk_file.name}"
        external_meta_url = f"{asset_url_base}/{meta_file.name}"
        # Newick is fetched at runtime — pass empty string; only meta matters here.
        newick = ""
    else:
        newick = nwk_file.read_text(encoding="utf-8").strip()
        if newick.endswith(";"):
            newick = newick[:-1]
        external_nwk_url  = None
        external_meta_url = None

    html = phylocanvas_html(
        newick, meta, container_id, height, tree_type,
        drilldown=drilldown,
        family_hover=True,
        subtrees_url_base=subtrees_url_base,
        external_nwk_url=external_nwk_url,
        external_meta_url=external_meta_url,
    )

    if fallback_img and fallback_img.exists():
        img_rel = "/" + fallback_img.relative_to(REPO).as_posix()
        noscript = (
            f'<noscript>'
            f'<img src="{img_rel}" alt="Evolutionary tree (static fallback)"'
            f' style="max-width:100%;" />'
            f'</noscript>'
        )
        html = html.replace(
            "</div></div>\n<script>",
            f"</div></div>\n{noscript}\n<script>",
            1,
        )
    return html


# ---------------------------------------------------------------------------
# Helpers: find and replace tagged cells in the markdown
# ---------------------------------------------------------------------------

_CODE_FENCE_PAT = re.compile(r"```python\n(.*?)\n```", re.DOTALL)


def _replace_tagged_cells(md: str) -> str:
    """Replace code fence blocks for tagged phylo cells with Phylocanvas embeds."""
    nb = _load_nb()

    ord_cells = cells_with_tag(nb, "phylo-order-tree")
    fam_cells = cells_with_tag(nb, "phylo-family-tree")

    ord_sources = {cell_to_str(c).strip() for c in ord_cells}
    fam_sources = {cell_to_str(c).strip() for c in fam_cells}

    def _repl(m: re.Match) -> str:
        code = m.group(1).strip()
        if code in ord_sources:
            return _build_phylocanvas_embed(
                nwk_file   = PHY_DIR / "order_tree.nwk",
                meta_file  = PHY_DIR / "order_meta.json",
                container_id = "avilist-ord-tree",
                height     = 580,
                tree_type  = "circular",
                fallback_img = IMG_DIR / "order_tree.png",
            )
        if code in fam_sources:
            return _build_phylocanvas_embed(
                nwk_file         = PHY_DIR / "family_tree.nwk",
                meta_file        = PHY_DIR / "family_meta.json",
                container_id     = "avilist-fam-tree",
                height           = 760,
                tree_type        = "circular",
                fallback_img     = IMG_DIR / "family_tree.png",
                drilldown        = True,
                subtrees_url_base = "/assets/data-science/avilist/phylogeny/subtrees/",
            )
        return m.group(0)

    return _CODE_FENCE_PAT.sub(_repl, md)


def _drop_nbconvert_phylo_output_duplicates(md: str) -> str:
    """Remove the entire ``display_phylocanvas()`` output preserved by nbconvert.

    For tagged phylo cells ``_replace_tagged_cells()`` inserts a new
    fetch-based ``phylocanvas_html()`` embed in place of the Python code fence.
    However, nbconvert also emits the *cell outputs* (the ``display_phylocanvas()``
    iframe with all data inlined as ``&quot;``-encoded HTML) as a separate HTML
    block.  That block is now redundant — and enormous (the inline subtrees can be
    4+ MB on a single line).

    Start sentinel: a line containing ``"Legend — bird orders"`` and ``"&quot;"``
    and longer than 2 KB — the opening wrapper div + legend + start of the
    ``<iframe srcdoc="...">``.

    End sentinel: a line containing ``</iframe></div>`` — closes the srcdoc
    attribute and the ``display_phylocanvas()`` outer wrapper.
    """
    out_lines: list[str] = []
    dropping = False
    for line in md.splitlines(keepends=True):
        if not dropping:
            if (
                "Legend — bird orders" in line
                and "&quot;" in line
                and len(line) > 2000
            ):
                dropping = True
                if "</iframe></div>" in line:
                    dropping = False
                continue
            out_lines.append(line)
        else:
            if "</iframe></div>" in line:
                dropping = False
    return "".join(out_lines)


def _strip_first_balanced_raw_block(t: str) -> str | None:
    """If *t* starts with ``{% raw %}``, remove that tag and its matching ``{% endraw %}``.

    Returns the inner markdown plus any text after the closing tag, or ``None``
    if *t* does not start with a raw block or tags are unbalanced.
    """
    m_open = re.match(r"^\{\%\s*raw\s*\%\}\s*\n", t, flags=re.IGNORECASE)
    if not m_open:
        return None
    start_inner = m_open.end()
    depth = 1
    pos = start_inner
    ro = re.compile(r"\{%\s*raw\s*%\}")
    rc = re.compile(r"\{%\s*endraw\s*%\}")
    while depth > 0:
        mo = ro.search(t, pos)
        mc = rc.search(t, pos)
        if mc is None:
            return None
        if mo is not None and mo.start() < mc.start():
            depth += 1
            pos = mo.end()
        else:
            depth -= 1
            if depth == 0:
                inner = t[start_inner : mc.start()]
                return inner + t[mc.end() :]
            pos = mc.end()
    return None


def _normalize_leading_raw_wrappers(body: str) -> str:
    """Collapse accidental nested ``{% raw %}`` wrappers (e.g. from re-running ``md-only``).

    Strips balanced raw blocks from the start of the body, and also from
    immediately after a leading markdown title image ``![...](...)``, until no
    more leading raw blocks remain.
    """
    b = body
    while True:
        t = b.lstrip("\n")
        lead = b[: len(b) - len(t)]
        stripped = _strip_first_balanced_raw_block(t)
        if stripped is not None:
            b = lead + stripped
            continue
        m = re.match(r"^(!\[[^\]]*\]\([^)]*\)\s*(?:\n\s*)*\n)", t)
        if not m:
            return b
        prefix, rest = m.group(0), t[len(m.group(0)) :]
        stripped = _strip_first_balanced_raw_block(rest)
        if stripped is None:
            return b
        b = lead + prefix + stripped
        continue


def _wrap_body_liquid_raw(md: str) -> str:
    """Prevent Jekyll Liquid from parsing ``{{`` inside Plotly / Phylocanvas HTML+JS."""
    if not md.startswith("---"):
        return md
    end = md.find("\n---\n", 3)
    if end == -1:
        return md
    split = end + 5
    head, body = md[:split], md[split:]
    body = _normalize_leading_raw_wrappers(body)
    if body.lstrip().startswith("{% raw %}"):
        return head + body
    return head + "\n{% raw %}\n" + body.lstrip("\n") + "\n{% endraw %}\n"


_RAW_BLOCK_RE = re.compile(r"\n\{\%\s*raw\s*\%\}\n", re.IGNORECASE)


def _move_teaser_image_before_raw(md: str) -> str:
    """AcademicPages /data-science/ index uses auto-excerpt (first body block).

    If the first lines inside ``{% raw %}`` are an H1 then the title figure, move
    that figure to after front matter and before ``{% raw %}`` (same pattern as
    other collection posts). ``header.teaser`` alone does not populate the list.
    """
    m = _RAW_BLOCK_RE.search(md)
    if not m:
        return md
    body = md[m.end() :]
    url_esc = re.escape(TEASER_IMAGE_URL)
    inner = re.compile(rf"(?P<h># [^\n]+\n\n)(?P<img>!\[[^\]]*\]\({url_esc}\)\n)")
    m2 = inner.match(body)
    if not m2:
        return md
    return (
        md[: m.start()]
        + "\n"
        + m2.group("img")
        + md[m.start() : m.end()]
        + m2.group("h")
        + body[m2.end() :]
    )


def _pre_raw_has_teaser_image(pre: str) -> bool:
    return bool(re.search(rf"!\[[^\]]*\]\({re.escape(TEASER_IMAGE_URL)}\)", pre))


def _remove_first_teaser_md_line(s: str, url: str) -> str:
    return re.sub(
        rf"^!\[[^\]]*\]\({re.escape(url)}\)\s*\n",
        "",
        s,
        count=1,
        flags=re.MULTILINE,
    )


def _parse_front_matter_title(md: str) -> str | None:
    """Return the ``title:`` string value from YAML front matter, if present."""
    if not md.lstrip().startswith("---"):
        return None
    end = md.find("\n---\n", 3)
    if end == -1:
        return None
    inner = md[3:end]
    for line in inner.splitlines():
        stripped = line.strip()
        if not stripped.startswith("title:"):
            continue
        val = stripped.split(":", 1)[1].strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            q = val[0]
            core = val[1:-1]
            return core.replace("\\" + q, q).replace("\\\\", "\\")
        return val
    return None


def _strip_duplicate_page_title_heading_in_raw(md: str) -> str:
    """Remove ``# …`` immediately inside ``{% raw %}`` when it matches YAML ``title``."""
    yaml_title = _parse_front_matter_title(md)
    if not yaml_title:
        return md
    m_raw = re.search(r"\n\{\%\s*raw\s*\%\}\s*\n", md)
    if not m_raw:
        return md
    tail = md[m_raw.end() :]
    m_h1 = re.match(r"#\s+([^\n]+)\s*\n+", tail)
    if not m_h1:
        return md
    if m_h1.group(1).strip() != yaml_title.strip():
        return md
    return md[: m_raw.end()] + tail[m_h1.end() :]


def _ensure_teaser_line_before_raw(md: str) -> str:
    """When the notebook puts ``## Date`` / ``tags:`` between the H1 and teaser image,
    the listing excerpt would otherwise be the heading only. Force one
    ``![…](teaser)`` line after front matter and drop the first duplicate inside
    the raw-wrapped body.
    """
    if not md.lstrip().startswith("---"):
        return md
    end = md.find("\n---\n", 3)
    if end == -1:
        return md
    head = md[: end + 5]
    tail = md[end + 5 :]
    m = re.search(r"\n\{\%\s*raw\s*\%\}\s*\n", tail)
    if not m:
        return md
    pre = tail[: m.start()]
    raw_open = tail[m.start() : m.end()]
    inner_rest = tail[m.end() :]
    if not _pre_raw_has_teaser_image(pre):
        teaser = f"![AviList title image]({TEASER_IMAGE_URL})\n\n"
        pre = (pre.rstrip() + "\n\n" + teaser) if pre.strip() else teaser
    inner_rest = _remove_first_teaser_md_line(inner_rest, TEASER_IMAGE_URL)
    return head + pre + raw_open + inner_rest


def _make_figure_page(body_html: str) -> str:
    """Wrap a Plotly figure HTML fragment in a minimal full HTML page."""
    return (
        '<!DOCTYPE html>\n'
        '<html><head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<style>html,body{margin:0;padding:0;background:#fff;'
        'font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}</style>\n'
        '</head>\n'
        f'<body>\n{body_html}\n</body>\n'
        '</html>\n'
    )


def _make_iframe(div_id: str, iframe_width: int, iframe_height: int) -> str:
    return (
        f'<iframe src="{_FIGURE_ASSET_URL_BASE}/{div_id}.html"'
        f' style="width:min({iframe_width}px,100%);height:{iframe_height}px;'
        f'border:none;border-radius:8px;display:block;margin:1em auto;"'
        f' loading="lazy"></iframe>\n'
    )


_FIGURE_IFRAME_BLOCK_RE = re.compile(
    # Variant 1 — sunburst panzoom wrapper around the externalized iframe.
    r'<div\s+class="sunburst-panzoom-root"[^>]*>'
    r'<iframe\s+src="/assets/data-science/avilist/figures/[^"]+"[^>]*></iframe>'
    r'\s*\n</div>'
    r'|'
    # Variant 2 — bare iframe (e.g. choropleth + family picker).
    r'<iframe\s+src="/assets/data-science/avilist/figures/[^"]+"[^>]*></iframe>',
    re.DOTALL,
)

# nbconvert Matplotlib cells emit ``![alt](url)`` on its own line after the code fence;
# keep these outside collapsed ``<details>`` like externalized Plotly iframes.
_MARKDOWN_PNG_EMBED_RE = re.compile(
    r'(?:\r?\n[ \t]*)+\r?\n[ \t]*!\[[^\]]*\]\([^)]+\)[ \t]*(?=\r?\n)',
    re.MULTILINE,
)

_DETAILS_BLOCK_RE = re.compile(
    r'<details\s+markdown="1"\s+class="avilist-setup-code">[\s\S]*?</details>',
    re.DOTALL,
)


def _lift_externalized_figures_outside_details(md: str) -> str:
    """Pull externalized figures out of their enclosing setup-code ``<details>``.

    ``_externalize_plotly_figures()`` replaces inline Plotly blobs with
    ``<iframe src="…/figures/…">`` tags.  When the surrounding code cell is
    wrapped by a ``<details markdown="1" class="avilist-setup-code">`` block via
    the notebook's markdown cells, the iframe ends up inside the collapsible —
    which hides the interactive chart by default along with the source code.
    This pass detects those iframes (optionally with a wrapping ``<div>``) and
    re-emits them immediately after the closing ``</details>``, so the code stays
    collapsed but the chart is visible.

    The same pass lifts nbconvert **markdown PNG** embeds (``![…](…)``) so
    Matplotlib figures stay visible when a whole notebook cell is wrapped in
    ``avilist-setup-code`` details.
    """

    def _rewrite_details(m: re.Match) -> str:
        block = m.group(0)
        figures: list[str] = []

        def _extract(fm: re.Match) -> str:
            figures.append(fm.group(0))
            return ""

        cleaned = _FIGURE_IFRAME_BLOCK_RE.sub(_extract, block)
        cleaned = _MARKDOWN_PNG_EMBED_RE.sub(_extract, cleaned)
        if not figures:
            return block
        return cleaned + "\n\n" + "\n\n".join(figures)

    return _DETAILS_BLOCK_RE.sub(_rewrite_details, md)


_AVILIST_SETUP_DETAILS_OPEN = '<details markdown="1" class="avilist-setup-code">'
_AVILIST_SETUP_DETAILS_CLOSE = "</details>"
# Summary line matches the hand-authored setup blocks (blank lines before the fence).
_AVILIST_CODE_SUMMARY_BLOCK = "<summary>Show code</summary>\n\n\n"
_ATX_HEADING_LINE_RE = re.compile(r"^#{1,6}\s")


def _line_is_atx_heading(line: str) -> bool:
    """True for a Markdown ATX heading at column 0 (nbconvert cell text uses indentation)."""
    if not line or line[0] in " \t" or line.startswith("    "):
        return False
    return bool(_ATX_HEADING_LINE_RE.match(line))


def _wrap_bare_python_fences_in_avilist_details(md: str) -> str:
    """Wrap each bare `` ```python `` fence + following cell output in collapsible details.

    Jupyter / nbconvert emits Python cells as plain fenced blocks.  Authors can
    optionally wrap cells in ``<details class="avilist-setup-code">`` inside the
    notebook markdown — but on a plain re-export those wrappers are absent.
    This pass restores the same HTML structure used for setup cells so the
    published post stays readable.

    Idempotent: fences that already sit inside an ``avilist-setup-code`` details
    block (net open/close depth before the opening `` ```python `` line) are left
    untouched.

    Cell output is everything after the closing `` ``` `` until the first line
    that looks like (a) a Markdown image ``![…](…)``, (b) an ATX heading
    ``# …`` at column 0, (c) the next fenced code block, or (d) another
    ``avilist-setup-code`` details opener.  Matplotlib PNG lines are left
    *outside* the details so they stay visible when collapsed; Plotly blobs are
    kept inside until :func:`_externalize_plotly_figures` and
    :func:`_lift_externalized_figures_outside_details` run next.
    """
    lines = md.splitlines(keepends=True)
    out: list[str] = []
    i, n = 0, len(lines)
    depth = 0
    n_wrapped = 0

    while i < n:
        line = lines[i]
        st = line.strip()
        if st == _AVILIST_SETUP_DETAILS_OPEN:
            depth += 1
            out.append(line)
            i += 1
            continue
        if st == _AVILIST_SETUP_DETAILS_CLOSE:
            depth = max(0, depth - 1)
            out.append(line)
            i += 1
            continue

        if st == "```python" and depth == 0:
            n_wrapped += 1
            out.append(_AVILIST_SETUP_DETAILS_OPEN + "\n")
            out.append(_AVILIST_CODE_SUMMARY_BLOCK)
            out.append(line)
            i += 1
            while i < n and lines[i].strip() != "```":
                out.append(lines[i])
                i += 1
            if i >= n:
                sys.stderr.write("[avilist] ERROR: unclosed ```python fence while wrapping details\n")
                break
            out.append(lines[i])
            i += 1

            tail: list[str] = []
            while i < n:
                L = lines[i]
                lst = L.strip()
                if lst.startswith("![") and "](" in lst:
                    break
                if _line_is_atx_heading(L):
                    break
                if lst.startswith("```"):
                    break
                if lst == _AVILIST_SETUP_DETAILS_OPEN:
                    break
                tail.append(L)
                i += 1
            out.extend(tail)
            out.append(_AVILIST_SETUP_DETAILS_CLOSE + "\n\n")
            continue

        out.append(line)
        i += 1

    if n_wrapped:
        print(f"[avilist] Wrapped {n_wrapped} bare python code fence(s) in collapse details")
    return "".join(out)


def _externalize_plotly_figures(md: str) -> str:
    """Replace inline Plotly figure blobs with ``<iframe>`` embeds.

    Handles two known patterns produced by ``avilist_birds_explore.ipynb``:

    1. **Sunburst** — wrapped in a ``sunburst_panzoom_viewport()`` div.  The
       panzoom outer ``<div id="sunburst-avilist-vp">`` opens before the Plotly
       CDN script, and the block ends with ``})();\\n</script></div>`` (the
       panzoom JS IIFE closing + outer div close).

    2. **Choropleth** — wrapped in a ``<div class="geo-family-picker">`` block
       followed by the Plotly CDN + div + init script + a family-picker IIFE
       ending with ``})();\\n</script>``.

    Each block is written to ``assets/data-science/avilist/figures/<id>.html``
    as a self-contained page and replaced in the post body with a small
    ``<iframe>`` tag.  The asset files live under ``assets/`` so Jekyll serves
    them verbatim (no Liquid processing).

    .. note::
        nbconvert emits the Python *source code* of display cells as markdown
        code fences.  Because those Python strings contain the same HTML markers
        (e.g. ``<div class="geo-family-picker">``), the regexes must **not**
        match content that is inside a code fence.  This function masks out all
        fenced code blocks before running the patterns, then restores them.
    """
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    # ── Mask code fences so patterns don't match Python source literals ────
    _fence_store: list[str] = []

    def _mask(m: re.Match) -> str:
        idx = len(_fence_store)
        _fence_store.append(m.group(0))
        return f"\x00FENCE{idx}\x00"

    masked = re.sub(r"```[\s\S]*?```", _mask, md)
    result = masked

    # ── 1. Sunburst panzoom block ──────────────────────────────────────────
    # The panzoom wrapper ends with  })();\n</script></div>  where the final
    # </div> closes <div id="sunburst-avilist-vp">.
    sunburst_re = re.compile(
        r'<div\s+id="sunburst-avilist-vp"[\s\S]*?\}\)\(\);\n</script></div>',
        re.DOTALL,
    )
    m = sunburst_re.search(result)
    if m:
        block = m.group(0)
        page  = _make_figure_page(block)
        dest  = FIGURE_DIR / "sunburst-avilist.html"
        dest.write_text(page, encoding="utf-8")
        print(f"[avilist] Externalized sunburst → {dest.name} ({len(page)//1024} KB)")
        # Square sunburst (~900px) + title/margins; iframe height avoids a large blank band below the figure.
        result = result[:m.start()] + _make_iframe("sunburst-avilist", 900, 1040) + result[m.end():]
    else:
        print("[avilist] WARNING: sunburst panzoom block not found — skipping externalization")

    # ── 2. Choropleth + family-picker block ────────────────────────────────
    # Starts at <div class="geo-family-picker"> and ends after the
    # family-picker IIFE  })();\n</script>  that follows the Plotly init.
    choropleth_re = re.compile(
        r'<div\s+class="geo-family-picker"[\s\S]*?\}\)\(\);\n</script>',
        re.DOTALL,
    )
    m = choropleth_re.search(result)
    if m:
        block = m.group(0)
        page  = _make_figure_page(block)
        dest  = FIGURE_DIR / "geo-choropleth.html"
        dest.write_text(page, encoding="utf-8")
        print(f"[avilist] Externalized choropleth → {dest.name} ({len(page)//1024} KB)")
        result = result[:m.start()] + _make_iframe("geo-choropleth", 900, 700) + result[m.end():]
    else:
        print("[avilist] WARNING: geo-choropleth family-picker block not found — skipping")

    # ── Restore masked code fences ─────────────────────────────────────────
    for idx, fence_text in enumerate(_fence_store):
        result = result.replace(f"\x00FENCE{idx}\x00", fence_text, 1)

    return result


# ---------------------------------------------------------------------------
# Main pipeline steps
# ---------------------------------------------------------------------------

def copy_assets() -> None:
    """Copy Newick + JSON files (and family subtrees) to the Jekyll assets directory."""
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    for fname in ("order_tree.nwk", "order_meta.json",
                  "family_tree.nwk", "family_meta.json"):
        src = PHY_DIR / fname
        if src.exists():
            shutil.copy2(src, ASSET_DIR / fname)

    # Copy per-family species subtrees so the static page can fetch() them on click.
    sub_src = PHY_DIR / "subtrees"
    sub_dst = ASSET_DIR / "subtrees"
    if sub_src.is_dir():
        sub_dst.mkdir(parents=True, exist_ok=True)
        for fpath in sub_src.iterdir():
            if fpath.is_file():
                shutil.copy2(fpath, sub_dst / fpath.name)
        print(f"[avilist] Copied {sum(1 for _ in sub_dst.iterdir())} subtree files → {sub_dst}")

    # Copy the subtrees index
    idx_src = PHY_DIR / "subtrees_index.json"
    if idx_src.exists():
        shutil.copy2(idx_src, ASSET_DIR / "subtrees_index.json")

    print(f"[avilist] Copied phylogeny assets → {ASSET_DIR}")

    title_src = AVILIST_ROOT / "assets" / "data-science" / "avilist" / "title.png"
    if title_src.is_file():
        IMG_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(title_src, IMG_DIR / title_src.name)
        print(f"[avilist] Copied teaser image → {IMG_DIR / title_src.name}")
    else:
        print(f"[avilist] NOTE: no teaser source at {title_src} (add in ebird-avilist repo)")

    _prune_stale_avilist_nbconvert_pngs()


def patch_md() -> None:
    """Load the markdown, apply all transformations, and write it back."""
    raw = MD.read_text(encoding="utf-8")
    raw = _apply_notebook_front_matter(raw)
    raw = _strip_lead_cell_meta_from_body(raw)
    raw = dedent_nbconvert_table_output(raw)

    # Math escaping (outside code fences)
    if raw.startswith("---"):
        end = raw.find("\n---\n", 3)
        if end != -1:
            fm   = raw[: end + 5]
            body = raw[end + 5:]
            body = process_outside_code_fences(body)
            raw  = fm + body
    else:
        raw = process_outside_code_fences(raw)

    # Fix relative image paths from nbconvert artefacts (older notebook runs used
    # ``2026-03-01-ebird-avilist`` as the output stem).
    for stem in (MD.stem, "ebird-avilist", "2026-03-01-ebird-avilist"):
        raw = raw.replace(f"{stem}_files/", "/images/data-science/avilist/")

    # Replace tagged phylo code blocks with Phylocanvas.gl embeds (fetch-based).
    raw = _replace_tagged_cells(raw)
    raw = _drop_nbconvert_phylo_output_duplicates(raw)
    # Re-apply collapsible wrappers around nbconvert code cells (idempotent if already wrapped).
    raw = _wrap_bare_python_fences_in_avilist_details(raw)

    # Externalize Plotly figure blobs to assets/ and replace with <iframe> tags.
    raw = _externalize_plotly_figures(raw)
    # Move those iframes out of their surrounding setup-code <details> blocks so
    # the chart is visible by default while the source code remains collapsed.
    raw = _lift_externalized_figures_outside_details(raw)

    raw = _wrap_body_liquid_raw(raw)
    raw = _move_teaser_image_before_raw(raw)
    raw = _ensure_teaser_line_before_raw(raw)
    raw = _strip_duplicate_page_title_heading_in_raw(raw)

    MD.write_text(raw, encoding="utf-8")
    print(f"[avilist] Patched markdown → {MD}")


def _prune_stale_avilist_nbconvert_pngs() -> None:
    """Remove nbconvert figure PNGs from a previous ``MD`` output stem (same notebook, new filename)."""
    current = MD.stem
    removed = 0
    for p in IMG_DIR.glob("*.png"):
        name = p.name
        if _LEGACY_NBCONVERT_PNG_RE.match(name):
            p.unlink(missing_ok=True)
            removed += 1
            continue
        m = _AVILIST_NBCONVERT_PNG_RE.match(name)
        if m and m.group("doc_stem") != current:
            p.unlink(missing_ok=True)
            removed += 1
    if removed:
        print(f"[avilist] Removed {removed} stale nbconvert PNG(s) under {IMG_DIR.name}/")


def sync_images() -> None:
    """Move nbconvert image artefacts into the standard images directory."""
    if not NB_FILES.is_dir():
        return
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for p in NB_FILES.glob("*.png"):
        shutil.copy2(p, IMG_DIR / p.name)
    shutil.rmtree(NB_FILES, ignore_errors=True)
    _prune_stale_avilist_nbconvert_pngs()
    print(f"[avilist] Synced images → {IMG_DIR}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    if not NB.is_file():
        sys.stderr.write(
            f"AviList notebook not found:\n  {NB}\n"
            "Clone the ebird-avilist repo next to this one (../ebird-avilist) or set "
            "EBIRD_AVILIST_ROOT to its root path.\n"
        )
        return 1

    if len(argv) > 1 and argv[1] == "md-only":
        copy_assets()
        patch_md()
        return 0

    # Full run
    run_nbconvert(NB, MD.parent, MD.stem)
    sync_images()
    copy_assets()
    patch_md()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
