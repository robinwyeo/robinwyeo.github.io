"""Shared utilities for nbconvert post-process scripts.

Functions here are imported by ``nbconvert_clt_postprocess.py`` and
``nbconvert_avilist_postprocess.py``.  Keep this module free of
notebook-specific logic.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Newick Kramdown / math helpers (shared between all post-process scripts)
# ---------------------------------------------------------------------------

def dollar_inline_to_paren(text: str) -> str:
    """Replace ``$...$`` with ``\\(...\\)``, leaving ``$$...$$`` unchanged."""
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
    """Kramdown treats ``\\(`` as literal ``(``: emit ``\\\\(`` for MathJax."""
    out: list[str] = []
    i = 0
    n = len(s)
    while i < n:
        if s.startswith("\\\\(", i):
            out.append("\\\\("); i += 3
        elif s.startswith("\\(", i):
            out.append("\\\\("); i += 2
        elif s.startswith("\\\\)", i):
            out.append("\\\\)"); i += 3
        elif s.startswith("\\)", i):
            out.append("\\\\)"); i += 2
        else:
            out.append(s[i]); i += 1
    return "".join(out)


def kramdown_inline_math_fixes(s: str) -> str:
    """Avoid ``[ ]`` inside ``\\(...\\)`` being parsed as Markdown links."""
    s = s.replace("\\(\\mu = E[X_i]\\)", "\\(\\mu = E\\text{[}X_{i}\\text{]}\\)")
    s = s.replace("\\(E[|X|] = \\infty\\)", "\\(E\\text{[}|X|\\text{]} = \\infty\\)")
    s = s.replace("\\text{Var}(X_i)", "\\text{Var}(X_{i})")
    return s


def jekyll_math_from_nbconvert_markdown(text: str) -> str:
    """Convert nbconvert ``$``/``\\(`` prose to Kramdown-safe MathJax delimiters."""
    return double_mjx_delimiters(kramdown_inline_math_fixes(dollar_inline_to_paren(text)))


def process_outside_code_fences(md: str) -> str:
    """Apply Jekyll math escaping to prose sections, skipping code fences."""
    parts = md.split("```")
    for i in range(0, len(parts), 2):
        parts[i] = jekyll_math_from_nbconvert_markdown(parts[i])
    return "```".join(parts)


def dedent_nbconvert_table_output(text: str) -> str:
    """Remove nbconvert's 4-space indent before stdout so ``|`` tables parse as GFM."""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    n = len(lines)
    prefix = "    |"
    while i < n:
        if lines[i].startswith(prefix):
            j = i
            while j < n and lines[j].startswith(prefix):
                j += 1
            if j - i >= 3:
                for k in range(i, j):
                    out.append(lines[k][4:])
            else:
                out.extend(lines[i:j])
            i = j
            continue
        out.append(lines[i])
        i += 1
    return "".join(out)


# ---------------------------------------------------------------------------
# Notebook cell helpers
# ---------------------------------------------------------------------------

def cell_to_str(cell: dict) -> str:
    return "".join(cell.get("source", []))


def normalize_python_source(source: str) -> str:
    return source.replace("\r\n", "\n").strip("\n")


def cells_with_tag(nb: dict, tag: str) -> list[dict]:
    """Return all code cells whose metadata.tags list contains *tag*."""
    return [
        c for c in nb.get("cells", [])
        if c.get("cell_type") == "code"
        and tag in c.get("metadata", {}).get("tags", [])
    ]


# ---------------------------------------------------------------------------
# nbconvert runner
# ---------------------------------------------------------------------------

def run_nbconvert(nb_path: Path, output_dir: Path, output_stem: str) -> None:
    """Run ``jupyter nbconvert --to markdown`` for *nb_path*."""
    jupyter = shutil.which("jupyter")
    if not jupyter:
        raise SystemExit("jupyter not found on PATH")
    subprocess.run(
        [
            jupyter, "nbconvert",
            "--to", "markdown",
            "--output", output_stem,
            "--output-dir", str(output_dir),
            str(nb_path),
        ],
        check=True,
    )
