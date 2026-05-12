#!/usr/bin/env python3
"""AviList notebook → Jekyll-friendly Markdown.

The analysis notebooks and phylogeny cache live in a separate clone of the
``ebird-avilist`` repository. This script runs from **robinwyeo.github.io** and
writes ``_data_science/ebird-avilist.md`` plus static assets under ``assets/`` and
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
5. Write out the final ``.md`` file for Jekyll.

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
MD = REPO / "_data_science" / "ebird-avilist.md"
NB_FILES = REPO / "_data_science" / "ebird-avilist_files"
PHY_DIR = AVILIST_ROOT / "data" / "phylogeny"

# Jekyll collection front matter (nbconvert does not emit YAML).
JEKYLL_FRONT_MATTER = """---
title: "Exploring the consolidated AviList"
date: 2026-05-12
tags:
  - AviList
  - birds
  - taxonomy
  - conservation
permalink: /data-science/ebird-avilist/
---

"""
ASSET_DIR = REPO / "assets" / "data-science" / "avilist" / "phylogeny"
IMG_DIR = REPO / "images" / "data-science" / "avilist"

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
) -> str:
    """Return a self-contained HTML block for one Phylocanvas.gl tree (Jekyll)."""
    newick = nwk_file.read_text(encoding="utf-8").strip()
    meta   = json.loads(meta_file.read_text(encoding="utf-8"))
    if newick.endswith(";"):
        newick = newick[:-1]

    html = phylocanvas_html(
        newick, meta, container_id, height, tree_type,
        drilldown=drilldown,
        subtrees_url_base=subtrees_url_base,
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
    """Remove nbconvert-preserved HTML *output* after we inlined Phylocanvas HTML.

    For tagged phylo cells, ``nbconvert`` emits the code fence plus a separate
    line of escaped HTML from ``display()`` — we replace the fence with
    ``phylocanvas_html()`` output, so the extra line duplicates the widget.
    """
    out_lines: list[str] = []
    for line in md.splitlines(keepends=True):
        if (
            "Legend — bird orders" in line
            and "&quot;" in line
            and len(line) > 2000
        ):
            continue
        out_lines.append(line)
    return "".join(out_lines)


# ---------------------------------------------------------------------------
# Main pipeline steps
# ---------------------------------------------------------------------------

def copy_assets() -> None:
    """Copy Newick + JSON files (and family subtrees) to the Jekyll assets directory."""
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
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


def patch_md() -> None:
    """Load the markdown, apply all transformations, and write it back."""
    raw = MD.read_text(encoding="utf-8")
    if not raw.lstrip().startswith("---"):
        raw = JEKYLL_FRONT_MATTER + raw
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

    # Fix relative image paths from nbconvert artefacts
    raw = raw.replace(
        "ebird-avilist_files/",
        "/images/data-science/avilist/",
    )

    # Replace tagged phylo code blocks with Phylocanvas.gl embeds
    raw = _replace_tagged_cells(raw)
    raw = _drop_nbconvert_phylo_output_duplicates(raw)

    MD.write_text(raw, encoding="utf-8")
    print(f"[avilist] Patched markdown → {MD}")


def sync_images() -> None:
    """Move nbconvert image artefacts into the standard images directory."""
    if not NB_FILES.is_dir():
        return
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for p in NB_FILES.glob("*.png"):
        shutil.copy2(p, IMG_DIR / p.name)
    shutil.rmtree(NB_FILES, ignore_errors=True)
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
