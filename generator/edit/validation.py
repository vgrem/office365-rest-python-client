"""Post-generation validation for generated model files.

The generator writes into existing, hand-refactored modules, so a bad run can
silently corrupt them — the observed failure modes are a duplicated top-level
class, a duplicate member re-added inside a class, and unparseable output. This
module checks the rendered source *before* it is written so such a run fails
fast instead of shipping a broken file.
"""

from __future__ import annotations

import ast


class ValidationError(Exception):
    """Raised when a generated module fails validation."""


def validate_source(source: str, path: str = "<generated>") -> list[str]:
    """Return a list of problems found in a generated module's source.

    Detects syntax errors, duplicate top-level class definitions, and duplicate
    members within a class (property getters/setters aside). An empty list means
    the source is safe to write.
    """
    issues: list[str] = []
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as e:
        return [f"syntax error: {e}"]

    class_names = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
    for name in sorted({name for name in class_names if class_names.count(name) > 1}):
        issues.append(f"duplicate class definition: {name}")

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            issues.extend(_duplicate_members(node))

    try:
        compile(source, path, "exec")
    except (SyntaxError, ValueError) as e:  # pragma: no cover - ast.parse covers most
        issues.append(f"compile error: {e}")
    return issues


def _duplicate_members(class_node: ast.ClassDef) -> list[str]:
    """Duplicate method/property names in a class body (``@x.setter`` excluded)."""
    counts: dict[str, int] = {}
    for stmt in class_node.body:
        for name in _member_names(stmt):
            counts[name] = counts.get(name, 0) + 1
    return [f"duplicate member in {class_node.name}: {name}" for name, count in counts.items() if count > 1]


def _member_names(stmt: ast.stmt) -> list[str]:
    """The member name(s) a class statement defines (empty when it defines none)."""
    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
        # ``@name.setter`` / ``@name.deleter`` and ``@overload`` stubs re-use the
        # name on purpose; only the implementation counts.
        if any(_is_property_accessor(d) or _is_overload(d) for d in stmt.decorator_list):
            return []
        return [stmt.name]
    if isinstance(stmt, ast.Assign):
        return [target.id for target in stmt.targets if isinstance(target, ast.Name)]
    if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
        return [stmt.target.id]
    return []


def _is_property_accessor(decorator: ast.expr) -> bool:
    return isinstance(decorator, ast.Attribute) and decorator.attr in {"setter", "deleter", "getter"}


def _is_overload(decorator: ast.expr) -> bool:
    return (isinstance(decorator, ast.Name) and decorator.id == "overload") or (
        isinstance(decorator, ast.Attribute) and decorator.attr == "overload"
    )
