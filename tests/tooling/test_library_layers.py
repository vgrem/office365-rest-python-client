"""The runtime may not import a product model.

``office365.runtime`` is the layer every product package stands on, so an import the
other way round is a cycle waiting to happen: it works only while the product module
happens not to import back the runtime member that needs it. One such import was real --
``runtime/types/public_error`` named ``PublicErrorDetail`` in ``onedrive.operations`` -- so
the detail moved to ``runtime/types`` and the import moved with it. Seven product imports
were in the runtime before; five are left.

The five are a different kind of debt: the runtime's *path* machinery is partly defined
inside the products it serves (``onedrive.internal.paths``, ``teams.internal.paths``), and
``converters/named.py`` needs the SharePoint field type to name a SharePoint field. That
is a refactor of the path layer, not a move, so the rows below are listed rather than
fixed: the set may only shrink, and a new row fails here.
"""

from __future__ import annotations

import ast
from pathlib import Path

_RUNTIME = Path(__file__).resolve().parents[2] / "office365" / "runtime"
_FLOOR = {"office365.runtime", "office365.entity", "office365.azure_env", "office365.logger"}

# (file under office365/, package it imports)
_KNOWN = {
    ("runtime/converters/named.py", "office365.sharepoint.fields.coercion"),
    ("runtime/converters/named.py", "office365.sharepoint.fields.type"),
    ("runtime/paths/service_operation.py", "office365.onedrive.internal.paths.url"),
    ("runtime/paths/v4/entity.py", "office365.onedrive.internal.paths.children"),
    ("runtime/paths/v4/entity.py", "office365.teams.internal.paths.joined_teams"),
}


def _imports(path: Path) -> set[str]:
    """Every ``office365`` package a module names, however it names it."""
    found: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("office365."):
            found.add(node.module)
        elif isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names if alias.name.startswith("office365."))
    return found


def _offenders() -> set[tuple[str, str]]:
    """``(package, office365 package)`` for every import that leaves the floor."""
    found = set()
    for path in sorted(_RUNTIME.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        package = str(path.parent.relative_to(_RUNTIME.parent))
        for name in _imports(path):
            if ".".join(name.split(".")[:2]) not in _FLOOR:
                found.add((f"{package}/{path.name}", name))
    return found


def test_the_runtime_imports_no_product_model() -> None:
    assert _offenders() == _KNOWN
