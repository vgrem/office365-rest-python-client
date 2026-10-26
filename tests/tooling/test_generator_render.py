"""Offline tests for generated-source post-processing (quote normalization)."""

from __future__ import annotations

import ast

from generator.builders.render import normalize_quotes, ruff_normalize


def test_ruff_normalize_wraps_at_the_repo_line_length():
    """Generated code follows the project config, not ruff's 88-column default.

    Sorting imports for a file inside the repo must reach ``pyproject.toml``:
    ruff's defaults would re-wrap every long import, so a one-property update
    rewrote dozens of untouched lines.
    """
    ruff_default_line_length = 88  # what ruff uses when it finds no config
    long_import = (
        "from office365.sharepoint.publishing.amplify.clientamplifyanywhereresults import ClientAmplifyAnywhereResults"
    )
    assert len(long_import) > ruff_default_line_length

    assert ruff_normalize(f"{long_import}\n", "office365/probe.py").strip() == long_import


def test_normalizes_to_double_quotes():
    assert normalize_quotes("x = self.properties.get('Title', None)\n") == 'x = self.properties.get("Title", None)\n'


def test_keeps_single_quotes_when_value_contains_double_quote():
    source = "x = 'say \"hi\"'\n"
    assert normalize_quotes(source) == source


def test_preserves_docstrings():
    source = 'def f():\n    """a "doc" """\n    return 1\n'
    assert normalize_quotes(source) == source


def test_output_still_parses():
    source = "x = {'a': 1, 'b': 'it\\'s'}\n"
    assert ast.parse(normalize_quotes(source)) is not None
