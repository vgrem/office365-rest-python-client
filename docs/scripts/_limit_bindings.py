"""Scan the source for ``@limit`` / ``@bounded`` bindings (docs helper).

Returns ``{limit_attr_name: ["Class.method", ...]}`` — the attribute name of the
limit expression (e.g. ``Limits.LIST_VIEW`` -> ``"LIST_VIEW"``) mapped to the
methods/properties that declare it. Pure ``ast`` (no imports, no side effects),
so the docs build doesn't import the whole package.
"""

from __future__ import annotations

import ast
import pathlib
from typing import Optional

_DECORATORS = {"limit", "bounded"}


def _limit_attr_name(node: ast.expr) -> Optional[str]:
    """The ``X`` in ``Limits.X`` / ``GraphLimits.X`` (the limit expression)."""
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def scan_bindings(root: pathlib.Path) -> dict[str, list[str]]:
    """Map each declared limit (by attribute name) to where it's bound."""
    result: dict[str, list[str]] = {}
    for path in sorted(root.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for cls in (node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)):
            for item in cls.body:
                if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                for dec in item.decorator_list:
                    if not (isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name) and dec.func.id in _DECORATORS):
                        continue
                    for arg in dec.args:
                        name = _limit_attr_name(arg)
                        if name is not None:
                            result.setdefault(name, []).append(f"{cls.name}.{item.name}")
    return result
