"""The Outlook codec's fixtures: a sidecar on disk, and the document it renders to.

A golden is compared byte for byte, so it lives beside its sidecar instead of inside a
Python string literal. The sidecar is JSON — what an export writes, and what an import
reads back — and the document is the bytes the writer produced, so a diff shows the
folded lines one per line rather than one wall of ``\\r\\n`` and ``\\\\;``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

FIXTURES = Path(__file__).parent / "fixtures" / "outlook"


def sidecar(name: str) -> dict[str, Any]:
    """A sidecar envelope by file stem: the record as an export wrote it."""
    return json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))


def document(name: str) -> bytes:
    """A golden document by file name: the bytes the writer rendered, CRLF and folding included."""
    return (FIXTURES / name).read_bytes()


__all__ = ["FIXTURES", "document", "sidecar"]
