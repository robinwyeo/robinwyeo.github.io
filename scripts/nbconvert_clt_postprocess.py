#!/usr/bin/env python3
"""CLT notebook → Jekyll-friendly Markdown.

Notebook (.ipynb) keeps GitHub/Jupyter-friendly ``$...$`` inline math. Exported
``.md`` is transformed for Kramdown/MathJax: ``$`` → ``\\(``, bracket fixes,
then ``\\\\(`` / ``\\\\)`` so Jekyll does not strip delimiters.
"""
from __future__ import annotations

import ast
import html
import io
import json
import keyword
import math
import re
import tokenize
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NB = (
    REPO
    / "_data_science"
    / "central-limit-theorem"
    / "2024-12-15-central-limit-theorem.ipynb"
)
MD = REPO / "_data_science" / "2024-12-15-central-limit-theorem.md"
IMG_DIR = REPO / "images" / "data-science" / "central-limit-theorem"
NB_FILES = REPO / "_data_science" / "2024-12-15-central-limit-theorem_files"
SETUP_TAG = "setup"

INTRO_NEW = (
    "*Jupyter notebook exploring the Central Limit Theorem. "
    "On the website this is a static page; interactive sliders run only in the "
    "[notebook source]"
    "(https://github.com/robinwyeo/robinwyeo.github.io/blob/master/"
    "_data_science/central-limit-theorem/2024-12-15-central-limit-theorem.ipynb).*\n"
)

INTRO_OLD = (
    "*Jupyter Notebook I wrote exploring the Central Limit Theorem to deepend my own "
    "understanding of own of my favorite equations in mathematics*\n"
)

DICE_OLD = (
    "- The interactive plot lets you adjust n and watch the sample means transition "
    "from the original uniform distribution (n=1) to an increasingly bell-shaped "
    "(normal) curve (with large n).\n"
    "\n"
    "Try sliding the sampole size (n) bar below to see how the distribution of the "
    "sample mean becomes normal as n grows large!"
)

DICE_NEW = (
    "- The interactive plot in the notebook lets you adjust $n$ and watch the sample "
    "means transition from the original uniform distribution ($n=1$) to an "
    "increasingly bell-shaped (normal) curve for large $n$.\n"
    "- Below, static figures show representative behavior at several values of $n$."
)


def paren_inline_to_dollar(text: str) -> str:
    r"""Turn ``\(...\)`` into ``$...$`` for notebook readability; leave ``$$`` blocks."""
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        if text.startswith("$$", i):
            j = text.find("$$", i + 2)
            if j < 0:
                out.append(text[i])
                i += 1
                continue
            out.append(text[i : j + 2])
            i = j + 2
        elif text.startswith("\\(", i) and not text.startswith("\\\\(", i):
            j = i + 2
            found = False
            while j < n - 1:
                if text[j] == "\\" and text[j + 1] == ")":
                    inner = text[i + 2 : j]
                    out.append("$" + inner + "$")
                    i = j + 2
                    found = True
                    break
                j += 1
            if not found:
                out.append(text[i])
                i += 1
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def simplify_notebook_math_notation(text: str) -> str:
    """Readable expectation / variance notation in ``$...$`` for GitHub preview."""
    text = text.replace(
        "$\\mu = E\\text{[}X_{i}\\text{]}$", "$\\mu = E[X_i]$"
    )
    text = text.replace(
        "$E\\text{[}|X|\\text{]} = \\infty$", "$E[|X|] = \\infty$"
    )
    return text


def dollar_inline_to_paren(text: str) -> str:
    """Replace $...$ with \\(...\\), leaving $$...$$ unchanged."""
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        if text.startswith("$$", i):
            j = text.find("$$", i + 2)
            if j < 0:
                out.append(text[i])
                i += 1
                continue
            out.append(text[i : j + 2])
            i = j + 2
        elif text[i] == "$":
            j = text.find("$", i + 1)
            if j < 0:
                out.append(text[i])
                i += 1
                continue
            out.append("\\(" + text[i + 1 : j] + "\\)")
            i = j + 1
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def double_mjx_delimiters(s: str) -> str:
    """Kramdown treats \\ ( as literal '(': emit \\\\( so HTML still contains \\(."""
    out: list[str] = []
    i = 0
    n = len(s)
    while i < n:
        if s.startswith("\\\\(", i):
            out.append("\\\\(")
            i += 3
        elif s.startswith("\\(", i):
            out.append("\\\\(")
            i += 2
        elif s.startswith("\\\\)", i):
            out.append("\\\\)")
            i += 3
        elif s.startswith("\\)", i):
            out.append("\\\\)")
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def kramdown_inline_math_fixes(s: str) -> str:
    """Avoid [ ] inside \\(...\\) being parsed as Markdown links."""
    s = s.replace(
        "\\(\\mu = E[X_i]\\)", "\\(\\mu = E\\text{[}X_{i}\\text{]}\\)"
    )
    s = s.replace(
        "\\(E[|X|] = \\infty\\)", "\\(E\\text{[}|X|\\text{]} = \\infty\\)"
    )
    # Subscripts beside punctuation: prefer explicit braces for kramdown emphasis rules
    s = s.replace("\\text{Var}(X_i)", "\\text{Var}(X_{i})")
    return s


def jekyll_math_from_nbconvert_markdown(text: str) -> str:
    """nbconvert ``$`` / ``\\(`` prose → Kramdown-safe MathJax delimiters in ``.md``."""
    return double_mjx_delimiters(kramdown_inline_math_fixes(dollar_inline_to_paren(text)))


def process_outside_code_fences(md: str) -> str:
    parts = md.split("```")
    for i in range(0, len(parts), 2):
        parts[i] = jekyll_math_from_nbconvert_markdown(parts[i])
    return "```".join(parts)


def _cell_to_str(cell: dict) -> str:
    return "".join(cell.get("source", []))


def _set_cell_source(cell: dict, text: str) -> None:
    lines = text.splitlines(keepends=True)
    if not lines:
        cell["source"] = ["\n"]
        return
    if not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    cell["source"] = lines


def _normalize_python_source(source: str) -> str:
    return source.replace("\r\n", "\n").strip("\n")


def _setup_fallback_sources(nb: dict, max_cells: int = 2) -> list[str]:
    """Fallback: first ``max_cells`` code cells under the ``## Setup`` heading."""
    cells = nb.get("cells", [])
    setup_heading_idx: int | None = None
    for idx, cell in enumerate(cells):
        if cell.get("cell_type") != "markdown":
            continue
        text = _cell_to_str(cell)
        if "## Setup" in text:
            setup_heading_idx = idx
            break
    if setup_heading_idx is None:
        return []

    setup_sources: list[str] = []
    for cell in cells[setup_heading_idx + 1 :]:
        cell_type = cell.get("cell_type")
        if cell_type == "markdown":
            text = _cell_to_str(cell).strip()
            # Stop once we reach the next substantial section heading.
            if text.startswith("#") and "Setup" not in text:
                break
            continue
        if cell_type != "code":
            continue
        setup_sources.append(_normalize_python_source(_cell_to_str(cell)))
        if len(setup_sources) >= max_cells:
            break
    return setup_sources


def tagged_code_sources(tag: str) -> list[str]:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    tagged: list[str] = []
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        tags = cell.get("metadata", {}).get("tags", [])
        if tag not in tags:
            continue
        tagged.append(_normalize_python_source(_cell_to_str(cell)))
    if tagged:
        return tagged
    return _setup_fallback_sources(nb)


def fix_notebook() -> None:
    """Keep ``$...$`` inline math in the ipynb (GitHub/Jupyter); do not apply Jekyll escapes."""
    nb = json.loads(NB.read_text(encoding="utf-8"))
    for cell in nb["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        text = _cell_to_str(cell)
        text = text.replace(INTRO_OLD, INTRO_NEW)
        text = text.replace(DICE_OLD, DICE_NEW)
        text = paren_inline_to_dollar(text)
        text = simplify_notebook_math_notation(text)
        _set_cell_source(cell, text)
    NB.write_text(json.dumps(nb, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_nbconvert() -> None:
    jupyter = shutil.which("jupyter")
    if not jupyter:
        raise SystemExit("jupyter not found on PATH")
    subprocess.run(
        [
            jupyter,
            "nbconvert",
            "--to",
            "markdown",
            "--output",
            MD.stem,
            "--output-dir",
            str(MD.parent.relative_to(REPO)),
            str(NB.relative_to(REPO)),
        ],
        cwd=REPO,
        check=True,
    )


def sync_images() -> None:
    if not NB_FILES.is_dir():
        return
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for p in NB_FILES.glob("*.png"):
        shutil.copy2(p, IMG_DIR / p.name)
    shutil.rmtree(NB_FILES, ignore_errors=True)


def _numeric_ast_value(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _numeric_ast_value(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp):
        left = _numeric_ast_value(node.left)
        right = _numeric_ast_value(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Pow):
            return left**right
        raise ValueError("unsupported binary operator")
    if isinstance(node, ast.Call) and len(node.args) == 1:
        func = node.func
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            if func.value.id in {"np", "math"} and func.attr == "sqrt":
                return math.sqrt(_numeric_ast_value(node.args[0]))
        raise ValueError("unsupported function call")
    raise ValueError("unsupported AST for numeric value")


def _python_literal_value(node: ast.AST) -> str | int | float | None:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (str, int, float)):
            return node.value
        return None
    try:
        return _numeric_ast_value(node)
    except ValueError:
        return None


def _default_interactive_config(distribution: str) -> dict[str, str | int | float]:
    defaults = {
        "dice": {
            "popMean": 3.5,
            "popStd": math.sqrt(35.0 / 12.0),
            "title": "CLT with Dice Rolls (Discrete Uniform)",
            "rawLabel": "Single roll (n = 1)",
            "nDefault": 1,
            "seed": 42,
            "trials": 2500,
            "fillColor": "rgba(53, 120, 160, 0.68)",
        },
        "exponential": {
            "popMean": 1.0,
            "popStd": 1.0,
            "title": "CLT with Exponential Distribution (Wait Times)",
            "rawLabel": "Single draw (n = 1)",
            "nDefault": 1,
            "seed": 84,
            "trials": 2500,
            "fillColor": "rgba(47, 150, 130, 0.68)",
        },
        "mixture": {
            "popMean": 2.3,
            "popStd": math.sqrt(20.11),
            "title": "CLT with the Bizarre Bimodal Mixture",
            "rawLabel": "Single draw (n = 1)",
            "nDefault": 1,
            "seed": 126,
            "trials": 2500,
            "fillColor": "rgba(124, 95, 165, 0.68)",
        },
    }
    return defaults.get(distribution, defaults["dice"]).copy()


def _json_string_value(value: str | int | float) -> str:
    return json.dumps(value, ensure_ascii=False)


def _extract_interactive_call_config(code: str) -> dict[str, str | int | float] | None:
    try:
        module = ast.parse(code)
    except SyntaxError:
        return None
    if len(module.body) != 1 or not isinstance(module.body[0], ast.Expr):
        return None
    expr = module.body[0].value
    if not isinstance(expr, ast.Call):
        return None
    if not isinstance(expr.func, ast.Name) or expr.func.id != "clt_plotly_interactive":
        return None

    kwargs: dict[str, str | int | float] = {}
    for keyword in expr.keywords:
        if keyword.arg is None:
            continue
        literal = _python_literal_value(keyword.value)
        if literal is not None:
            kwargs[keyword.arg] = literal
    if "distribution" not in kwargs or not isinstance(kwargs["distribution"], str):
        return None

    distribution = str(kwargs["distribution"])
    config = _default_interactive_config(distribution)
    config["distribution"] = distribution

    mapped_fields = {
        "pop_mean": "popMean",
        "pop_std": "popStd",
        "title": "title",
        "raw_label": "rawLabel",
        "n_default": "nDefault",
        "seed": "seed",
        "trials": "trials",
        "bar_color": "fillColor",
    }
    for src_key, dst_key in mapped_fields.items():
        if src_key in kwargs:
            config[dst_key] = kwargs[src_key]

    return config


def _interactive_embed_html(config: dict[str, str | int | float], idx: int) -> str:
    distribution = str(config.get("distribution", "plot"))
    container_id = f"clt-interactive-{distribution}-{idx}"
    config_js = ", ".join(
        f"{k}: {_json_string_value(v)}"
        for k, v in [
            ("distribution", config["distribution"]),
            ("popMean", config["popMean"]),
            ("popStd", config["popStd"]),
            ("title", config["title"]),
            ("rawLabel", config["rawLabel"]),
            ("nDefault", config["nDefault"]),
            ("seed", config["seed"]),
            ("trials", config["trials"]),
            ("fillColor", config["fillColor"]),
        ]
    )
    return (
        f'<div id="{container_id}"></div>\n'
        "<script>\n"
        "(function(){\n"
        "  function renderWidget(){\n"
        "    if (window.renderCLTInteractivePlot) {\n"
        f'      window.renderCLTInteractivePlot("{container_id}", {{ {config_js} }});\n'
        "    }\n"
        "  }\n"
        "  if (window.renderCLTInteractivePlot) {\n"
        "    renderWidget();\n"
        "    return;\n"
        "  }\n"
        "  var existing = document.querySelector('script[data-clt-interactive-loader=\"true\"]');\n"
        "  if (!existing) {\n"
        "    existing = document.createElement('script');\n"
        "    existing.src = '/assets/js/clt-interactive.js';\n"
        "    existing.defer = true;\n"
        "    existing.setAttribute('data-clt-interactive-loader', 'true');\n"
        "    document.head.appendChild(existing);\n"
        "  }\n"
        "  existing.addEventListener('load', renderWidget, { once: true });\n"
        "  if (window.renderCLTInteractivePlot) {\n"
        "    renderWidget();\n"
        "  }\n"
        "}());\n"
        "</script>"
    )


def replace_interactive_plot_blocks(md: str) -> str:
    pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)
    counter = 0

    def _repl(match: re.Match[str]) -> str:
        nonlocal counter
        code = match.group(1)
        if "clt_plotly_interactive(" not in code:
            return match.group(0)
        config = _extract_interactive_call_config(code)
        if not config:
            return match.group(0)
        counter += 1
        return _interactive_embed_html(config, counter)

    return pattern.sub(_repl, md)


def _builtin_names() -> set[str]:
    import builtins

    return {n for n in dir(builtins) if not n.startswith("_")}


def _fstring_token_types() -> frozenset[int]:
    if getattr(tokenize, "FSTRING_START", None) is None:
        return frozenset()
    return frozenset(
        {
            tokenize.FSTRING_START,
            tokenize.FSTRING_MIDDLE,
            tokenize.FSTRING_END,
        }
    )


def _highlight_python_for_jekyll(code: str) -> str:
    """Same wrapper Rouge uses for `` ```python `` so site SCSS applies."""

    def wrap_body(inner: str) -> str:
        return (
            '<div class="language-python highlighter-rouge">'
            '<div class="highlight"><pre class="highlight"><code>'
            f"{inner}</code></pre></div></div>"
        )

    text = code.replace("\r\n", "\n")
    if not text.endswith("\n"):
        text += "\n"

    builtins = _builtin_names()
    fstring_types = _fstring_token_types()
    punct_ops = set("()[]{}:,.;@")

    def op_class(op: str) -> str:
        return "p" if op in punct_ops else "o"

    lines = text.splitlines(keepends=True)
    line_starts: list[int] = []
    acc = 0
    for line in lines:
        line_starts.append(acc)
        acc += len(line)

    def pos_index(line: int, col: int) -> int:
        return line_starts[line - 1] + col

    out: list[str] = []
    prev_idx = 0

    def span(cls: str, piece: str) -> None:
        out.append(f'<span class="{cls}">{html.escape(piece, quote=False)}</span>')

    readline = io.StringIO(text).readline
    after_def = False
    after_class = False
    try:
        for tok in tokenize.generate_tokens(readline):
            t = tok.type
            s = tok.string
            if t in (tokenize.ENDMARKER, tokenize.NL, tokenize.DEDENT):
                continue
            if t == tokenize.ENCODING:
                continue

            start_i = pos_index(tok.start[0], tok.start[1])
            if start_i > prev_idx:
                out.append(html.escape(text[prev_idx:start_i], quote=False))
            end_i = pos_index(tok.end[0], tok.end[1])
            prev_idx = end_i

            if t == tokenize.NAME:
                if after_def:
                    span("nf", s)
                    after_def = False
                elif after_class:
                    span("nc", s)
                    after_class = False
                elif keyword.iskeyword(s):
                    span("k", s)
                    if s == "def":
                        after_def = True
                    elif s == "class":
                        after_class = True
                elif s in ("True", "False", "None"):
                    span("kc", s)
                elif s in builtins:
                    span("nb", s)
                else:
                    span("n", s)
            elif t == tokenize.NUMBER:
                span("mi", s)
            elif t == tokenize.STRING:
                span("s2", s)
            elif t in fstring_types:
                span("s2", s)
            elif t == tokenize.COMMENT:
                span("c1", s)
            elif t == tokenize.OP:
                span(op_class(s), s)
            elif t == tokenize.NEWLINE:
                out.append("\n")
            elif t == tokenize.INDENT:
                out.append(html.escape(s, quote=False))
            elif t == tokenize.ERRORTOKEN:
                out.append(html.escape(s, quote=False))
            else:
                out.append(html.escape(s, quote=False))
    except (tokenize.TokenError, SyntaxError):
        return wrap_body(html.escape(text.rstrip("\n"), quote=False))

    if prev_idx < len(text):
        out.append(html.escape(text[prev_idx:], quote=False))

    return wrap_body("".join(out))


def _setup_wrapper_block(code: str, idx: int) -> str:
    highlighted = _highlight_python_for_jekyll(code)
    return (
        f'<div class="setup-code-collapsible" data-setup-code-id="{idx}">\n'
        '  <button class="setup-code-toggle" type="button" aria-expanded="false">'
        "Show setup code</button>\n"
        '  <div class="setup-code-body" hidden>\n'
        f"    {highlighted}\n"
        "  </div>\n"
        "</div>"
    )


def wrap_tagged_setup_code_blocks(md: str, tagged_sources: list[str]) -> str:
    if not tagged_sources:
        return md

    pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)
    tagged_normalized = [_normalize_python_source(src) for src in tagged_sources]
    setup_cursor = 0
    wrapped_count = 0

    def _repl(match: re.Match[str]) -> str:
        nonlocal setup_cursor, wrapped_count
        if setup_cursor >= len(tagged_normalized):
            return match.group(0)

        code = match.group(1)
        if _normalize_python_source(code) != tagged_normalized[setup_cursor]:
            return match.group(0)

        setup_cursor += 1
        wrapped_count += 1
        return _setup_wrapper_block(code, wrapped_count)

    out = pattern.sub(_repl, md)
    if wrapped_count == 0:
        return out

    setup_assets = (
        "<style>\n"
        ".setup-code-collapsible { position: relative; margin: 1.2rem 0; }\n"
        ".setup-code-toggle { position: absolute; top: 0.55rem; right: 0.55rem; z-index: 2; border: 1px solid #c9d1d9; border-radius: 8px; background: #f6f8fa; color: #24292f; padding: 0.2rem 0.55rem; font-size: 0.82rem; cursor: pointer; }\n"
        ".setup-code-collapsible .highlighter-rouge { margin-bottom: 0; }\n"
        ".setup-code-collapsible .highlighter-rouge:before { display: none; }\n"
        "</style>\n"
        "<script>\n"
        "(function() {\n"
        "  function wireSetupToggles(root) {\n"
        "    root.querySelectorAll('.setup-code-toggle').forEach(function(btn) {\n"
        "      if (btn.dataset.bound === '1') return;\n"
        "      btn.dataset.bound = '1';\n"
        "      btn.addEventListener('click', function() {\n"
        "        var body = btn.parentElement.querySelector('.setup-code-body');\n"
        "        var isOpen = !body.hasAttribute('hidden');\n"
        "        if (isOpen) {\n"
        "          body.setAttribute('hidden', 'hidden');\n"
        "          btn.setAttribute('aria-expanded', 'false');\n"
        "          btn.textContent = 'Show setup code';\n"
        "        } else {\n"
        "          body.removeAttribute('hidden');\n"
        "          btn.setAttribute('aria-expanded', 'true');\n"
        "          btn.textContent = 'Hide setup code';\n"
        "        }\n"
        "      });\n"
        "    });\n"
        "  }\n"
        "  if (document.readyState === 'loading') {\n"
        "    document.addEventListener('DOMContentLoaded', function() { wireSetupToggles(document); });\n"
        "  } else {\n"
        "    wireSetupToggles(document);\n"
        "  }\n"
        "}());\n"
        "</script>\n"
    )
    # Jekyll only recognizes YAML front matter at the very start of the file.
    # Insert setup assets *after* a leading teaser image (if any) so the site
    # excerpt (first \\n\\n-separated block) stays the image for archive listings.
    teaser_after_fm = re.compile(
        r"^(?:[ \t]*\n)*!\[[^\]]*\]\([^)]+\)(?:[ \t]*\n)+", re.MULTILINE
    )

    if out.startswith("---"):
        fm_end = out.find("\n---\n", 3)
        if fm_end != -1:
            split_at = fm_end + 5
            rest = out[split_at:]
            m = teaser_after_fm.match(rest)
            if m:
                insert_at = split_at + m.end()
                return out[:insert_at] + setup_assets + out[insert_at:]
            return out[:split_at] + setup_assets + out[split_at:]
    return setup_assets + out


def patch_md_file() -> None:
    raw = MD.read_text(encoding="utf-8")
    setup_sources = tagged_code_sources(SETUP_TAG)
    if raw.startswith("---"):
        end = raw.find("\n---\n", 3)
        if end != -1:
            fm = raw[: end + 5]
            body = raw[end + 5 :]
            body = process_outside_code_fences(body)
            raw = fm + body
    else:
        raw = process_outside_code_fences(raw)
    raw = raw.replace(
        "2024-12-15-central-limit-theorem_files/",
        "/images/data-science/central-limit-theorem/",
    )
    raw = raw.replace(
        "/_data_science/central-limit-theorem/clt-interactive.js",
        "/assets/js/clt-interactive.js",
    )
    raw = replace_interactive_plot_blocks(raw)
    raw = wrap_tagged_setup_code_blocks(raw, setup_sources)
    raw = re.sub(
        r"\n```\n\n\n    VBox\(children=\(IntSlider\(value=30, continuous_update=False, description='Sample size n', layout=Layout\(width='…\n\n\n",
        "\n```\n\n",
        raw,
    )
    MD.write_text(raw, encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "notebook-only":
        fix_notebook()
        return 0
    if len(argv) > 1 and argv[1] == "md-only":
        patch_md_file()
        return 0
    fix_notebook()
    run_nbconvert()
    sync_images()
    patch_md_file()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
