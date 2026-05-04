#!/usr/bin/env python3
"""CLT notebook → Jekyll-friendly Markdown: inline math \\(...\\), images, cleanup."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NB = REPO / "_data_science" / "2024-12-15-central-limit-theorem.ipynb"
MD = REPO / "_data_science" / "2024-12-15-central-limit-theorem.md"
IMG_DIR = REPO / "images" / "data-science" / "central-limit-theorem"
NB_FILES = REPO / "_data_science" / "2024-12-15-central-limit-theorem_files"

INTRO_NEW = (
    "*Jupyter notebook exploring the Central Limit Theorem. "
    "On the website this is a static page; interactive sliders run only in the "
    "[notebook source]"
    "(https://github.com/robinwyeo/robinwyeo.github.io/blob/master/"
    "_data_science/2024-12-15-central-limit-theorem.ipynb).*\n"
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


def fix_markdown_prose(text: str) -> str:
    """Notebook / nbconvert output: single \\(. Kramdown needs \\\\( in .md for MathJax."""
    return kramdown_inline_math_fixes(dollar_inline_to_paren(text))


def process_outside_code_fences(md: str) -> str:
    parts = md.split("```")
    for i in range(0, len(parts), 2):
        parts[i] = double_mjx_delimiters(fix_markdown_prose(parts[i]))
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


def fix_notebook() -> None:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    for cell in nb["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        text = _cell_to_str(cell)
        text = text.replace(INTRO_OLD, INTRO_NEW)
        text = text.replace(DICE_OLD, DICE_NEW)
        _set_cell_source(cell, fix_markdown_prose(text))
    NB.write_text(json.dumps(nb, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_nbconvert() -> None:
    jupyter = shutil.which("jupyter")
    if not jupyter:
        raise SystemExit("jupyter not found on PATH")
    subprocess.run(
        [jupyter, "nbconvert", "--to", "markdown", str(NB.relative_to(REPO))],
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


def patch_md_file() -> None:
    raw = MD.read_text(encoding="utf-8")
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
