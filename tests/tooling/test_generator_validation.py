"""Offline tests for checking generated source: the validator and the post-commit verifier."""

from __future__ import annotations

from pathlib import Path

import pytest
from generator import verification as verification_module
from generator.validation import ValidationError, validate_source
from generator.verification import PostCommitVerifier, semantic_issues


def test_duplicate_class_definition_detected():
    source = "class A:\n    pass\n\n\nclass A:\n    pass\n"
    assert any("duplicate class" in issue for issue in validate_source(source))


def test_duplicate_member_detected():
    source = "class A:\n    def x(self):\n        return 1\n\n    def x(self):\n        return 2\n"
    assert any("duplicate member" in issue for issue in validate_source(source))


def test_property_setter_is_not_a_duplicate():
    source = (
        "class A:\n"
        "    @property\n"
        "    def x(self):\n"
        "        return self._x\n\n"
        "    @x.setter\n"
        "    def x(self, value):\n"
        "        self._x = value\n"
    )
    assert validate_source(source) == []


def test_syntax_error_detected():
    assert validate_source("class A(:\n    pass\n") != []


def test_overloads_are_not_duplicates():
    source = (
        "from typing import overload\n"
        "class A:\n"
        "    @overload\n"
        "    def x(self, n: int) -> int: ...\n"
        "    @overload\n"
        "    def x(self, n: str) -> str: ...\n"
        "    def x(self, n):\n"
        "        return n\n"
    )
    assert validate_source(source) == []


# -------------------------------------------------------------- post-commit verifier


class _Builder:
    def __init__(self, file: str) -> None:
        self.file = file


def test_module_name_derives_a_dotted_path(tmp_path: Path) -> None:
    verifier = PostCommitVerifier(tmp_path / "office365")

    assert verifier._module_name(str(tmp_path / "office365" / "a" / "b.py")) == "office365.a.b"
    assert verifier._module_name(str(tmp_path / "elsewhere" / "b.py")) is None


def test_smoke_import_raises_on_import_failure(tmp_path: Path, monkeypatch) -> None:
    verifier = PostCommitVerifier(tmp_path / "office365")
    builder = _Builder(str(tmp_path / "office365" / "thing.py"))

    def _boom(module: str):
        raise ImportError("boom")

    monkeypatch.setattr(verification_module.importlib, "import_module", _boom)
    with pytest.raises(ValidationError, match="failed to import"):
        verifier._smoke_import([("x", builder)])


def test_semantic_issues_flags_undefined_names(tmp_path: Path) -> None:
    issues = semantic_issues("def f():\n    return Missing\n", str(tmp_path / "x.py"))

    assert issues  # F821
    assert any("Missing" in issue for issue in issues)


def test_semantic_issues_accepts_clean_source(tmp_path: Path) -> None:
    assert semantic_issues("x = 1\n", str(tmp_path / "x.py")) == []
