"""Put the type a getter already names within reach of the runtime (one-time codemod).

``declared_type`` reads a getter's return annotation to decide how to coerce a wire
value, and it reads it through ``typing.get_type_hints``, which evaluates the
annotation text against the module's globals. A generated getter spells its type
locally instead::

    @odata(name="sourceEnvironment")
    @property
    def source_environment(self) -> BrowserSharedCookieSourceEnvironment:
        from office365.intune.browser.sharedcookiesourceenvironment import (
            BrowserSharedCookieSourceEnvironment,
        )

        return self.properties.get("sourceEnvironment", BrowserSharedCookieSourceEnvironment.microsoftEdge)

The name is written twice and visible to the runtime in neither place -- the
``if TYPE_CHECKING:`` block never executes, and a function-local import is gone by the
time the annotation is evaluated. ``declared_type`` therefore answers ``None``, and
``coerce_value`` has no reason to call ``parse_enum``: ``'2'`` stays the string ``'2'``
instead of becoming ``BrowserSharedCookieSourceEnvironment.both``.

The generator's own rule says such a name belongs at module level
(``generator/builders/property.py:needs_runtime_import``: a complex value uses
``field(default_factory=X)`` and an enum ``X.member``, both evaluated when the class is
built), but it writes imports once, when a file is first generated -- ``generate_model``
plans ``0 updated`` for these files today, so the tree has drifted from the rule. This
script closes the drift: it moves the import to the module block, drops the local copy,
and drops the now-dead ``TYPE_CHECKING`` entry.

Only imports that cannot close a cycle are hoisted. A cycle between generated types is
also a module import cycle, and the generator breaks it by keeping the reference
annotation-only (``generator/cycles.py``); the same test is applied here against the
module-level import graph -- a target module that can already reach the getter's module
would make the new edge a cycle, so it stays local. Enum and complex-value targets are
offered (``--only``), entity/navigation references are not: an entity getter builds its
child through a ``ResourcePath`` and imports the type lazily by design, and no untyped
column depends on one.

Usage::

    uv run python scripts/hoist_imports.py --dry-run
    uv run python scripts/hoist_imports.py --only enum
    uv run ruff check --fix office365   # sort the new imports
"""

from __future__ import annotations

import argparse
import ast
import importlib
import pathlib
import re
import sys
from typing import Dict, Iterator, List, NamedTuple, Optional, Sequence, Set, Tuple

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

_LINE_LENGTH = 121
_ROOT = pathlib.Path(__file__).resolve().parents[1]
_TARGET = _ROOT / "office365"


class Edit(NamedTuple):
    """A line range to replace (``end < start`` inserts before ``start``)."""

    start: int
    end: int
    lines: List[str]


class Site(NamedTuple):
    """One getter-local import of a name its own annotation spells."""

    module: str
    target: str
    name: str
    class_name: str
    getter: str
    wire: Optional[str]
    kind: str


def package_of(path: pathlib.Path) -> str:
    """Dotted module name for a file under ``office365``."""
    parts = list(path.relative_to(_ROOT).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def module_imports(path: pathlib.Path) -> Set[str]:
    """Modules ``path`` imports at run time (``TYPE_CHECKING`` blocks excluded)."""
    tree = ast.parse(path.read_text())

    def edges(statements: Sequence[ast.stmt]) -> Iterator[str]:
        for node in statements:
            if isinstance(node, ast.ImportFrom) and node.module:
                yield node.module
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    yield alias.name
            elif isinstance(node, ast.If):
                if isinstance(node.test, ast.Name) and node.test.id == "TYPE_CHECKING":
                    continue
                yield from edges(node.body)
                yield from edges(node.orelse)

    return {name for name in edges(tree.body) if name.startswith("office365")}


def import_graph() -> Dict[str, Set[str]]:
    """Module-level import graph over ``office365``, built once."""
    graph: Dict[str, Set[str]] = {}
    for path in _TARGET.rglob("*.py"):
        try:
            graph[package_of(path)] = module_imports(path)
        except SyntaxError:
            continue
    return graph


def closes_a_cycle(graph: Dict[str, Set[str]], target: str, module: str) -> bool:
    """Whether importing ``target`` from ``module`` would make an import cycle."""
    seen: Set[str] = set()
    todo = [target]
    while todo:
        node = todo.pop()
        if node == module:
            return True
        if node in seen:
            continue
        seen.add(node)
        todo.extend(edge for edge in graph.get(node, ()) if edge not in seen)
    return False


def kind_of(target: str, name: str) -> Optional[str]:
    """``enum`` / ``value`` / ``entity`` / ``other`` for the imported name."""
    from enum import Enum

    from office365.runtime.client_object import ClientObject
    from office365.runtime.client_value import ClientValue

    try:
        obj = getattr(importlib.import_module(target), name)
    except Exception:
        return None
    if not isinstance(obj, type):
        return "other"
    if issubclass(obj, Enum):
        return "enum"
    if issubclass(obj, ClientValue):
        return "value"
    if issubclass(obj, ClientObject):
        return "entity"
    return "other"


def is_property(node: ast.FunctionDef) -> bool:
    """Whether the function is a ``@property`` getter, possibly under ``@odata``."""
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id == "property":
            return True
        if isinstance(decorator, ast.Attribute) and decorator.attr == "property":
            return True
    return False


def wire_name(node: ast.FunctionDef) -> Optional[str]:
    """The OData name stated by the getter's own ``@odata(name=...)``, if any."""
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call) and getattr(decorator.func, "id", None) == "odata":
            for keyword in decorator.keywords:
                if keyword.arg == "name" and isinstance(keyword.value, ast.Constant):
                    return str(keyword.value.value)
    return None


def annotation_of(node: ast.FunctionDef) -> Optional[str]:
    """The getter's return annotation as the runtime sees it: source text."""
    if node.returns is None:
        return None
    if isinstance(node.returns, ast.Constant) and isinstance(node.returns.value, str):
        return node.returns.value
    return ast.unparse(node.returns)


def has_future_annotations(tree: ast.Module) -> bool:
    """Whether ``from __future__ import annotations`` makes annotation text legal."""
    return any(
        isinstance(node, ast.ImportFrom)
        and node.module == "__future__"
        and any(alias.name == "annotations" for alias in node.names)
        for node in tree.body
    )


def local_imports(node: ast.FunctionDef) -> List[ast.ImportFrom]:
    """``from … import …`` statements sitting at the top of the getter's body."""
    return [stmt for stmt in node.body if isinstance(stmt, ast.ImportFrom) and stmt.module]


def type_checking_block(tree: ast.Module) -> Optional[ast.If]:
    """The module's ``if TYPE_CHECKING:`` block, when it states one."""
    for node in tree.body:
        if isinstance(node, ast.If) and isinstance(node.test, ast.Name) and node.test.id == "TYPE_CHECKING":
            return node
    return None


def plan_module(path: pathlib.Path, only: Set[str]) -> Tuple[List[Site], List[str]]:
    """Every local import in ``path`` whose kind is wanted, and the ones it cannot read."""
    tree = ast.parse(path.read_text())
    if not has_future_annotations(tree):
        return [], []
    module = package_of(path)
    sites: List[Site] = []
    skipped: List[str] = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.FunctionDef) and is_property(node)):
            continue
        annotation = annotation_of(node)
        if annotation is None:
            continue
        statements = local_imports(node)
        if not statements:
            continue
        parent = _enclosing_class(tree, node)
        for statement in statements:
            for alias in statement.names:
                if not re.search(rf"\b{re.escape(alias.name)}\b", annotation):
                    continue
                where = f"{parent or module}.{node.name} imports {alias.name}"
                kind = kind_of(statement.module, alias.name)
                if kind is None:
                    skipped.append(f"{where} from an unimportable module {statement.module}")
                elif kind in only:
                    sites.append(
                        Site(module, statement.module, alias.name, parent or "", node.name, wire_name(node), kind)
                    )
    return sites, skipped


def _enclosing_class(tree: ast.Module, target: ast.FunctionDef) -> Optional[str]:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and target in node.body:
            return node.name
    return None


def apply(path: pathlib.Path, sites: List[Site]) -> int:
    """Write the hoist for one module and return the number of imports it moved."""
    tree = ast.parse(path.read_text())
    source = path.read_text().splitlines(keepends=True)
    hoisted = {(site.target, site.name) for site in sites}
    edits: List[Edit] = []

    block = type_checking_block(tree)
    if block is not None:
        _drop_from_block(block, hoisted, edits)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and is_property(node):
            for statement in local_imports(node):
                before = len(edits)
                _drop_from_statement(statement, hoisted, edits)
                _swallow_blank_line(source, edits, before)
    _insert_imports(tree, hoisted, edits)

    for edit in sorted(edits, key=lambda item: (item.start, item.end), reverse=True):
        source[edit.start - 1 : edit.end] = edit.lines
    path.write_text("".join(source))
    return len(hoisted)


def _drop_from_block(block: ast.If, hoisted: Set[Tuple[str, str]], edits: List[Edit]) -> None:
    """Remove hoisted names from ``if TYPE_CHECKING:``; remove the block when emptied.

    The block is planned whole and then edited once: a per-statement edit and a
    block-wide edit would describe overlapping line ranges, and the second one would
    apply to line numbers the first had already shifted.
    """
    plan: List[Tuple[ast.ImportFrom, List[ast.alias]]] = []
    remaining = 0
    for statement in block.body:
        if isinstance(statement, ast.ImportFrom) and statement.module:
            kept = [alias for alias in statement.names if (statement.module, alias.name) not in hoisted]
            remaining += len(kept)
            plan.append((statement, kept))
        else:
            remaining += 1
    if remaining == 0:
        edits.append(Edit(block.lineno, block.end_lineno or block.lineno, []))
        return
    for statement, kept in plan:
        if len(kept) == len(statement.names):
            continue
        if not kept:
            edits.append(Edit(statement.lineno, statement.end_lineno or statement.lineno, []))
            continue
        names = [alias.name if alias.asname is None else f"{alias.name} as {alias.asname}" for alias in kept]
        edits.append(
            Edit(statement.lineno, statement.end_lineno or statement.lineno, _import_lines(statement.module, names))
        )


def _drop_from_statement(statement: ast.ImportFrom, hoisted: Set[Tuple[str, str]], edits: List[Edit]) -> int:
    """Drop hoisted aliases from one statement, deleting it when nothing is left."""
    kept = [alias for alias in statement.names if (statement.module, alias.name) not in hoisted]
    if len(kept) == len(statement.names):
        return len(statement.names)
    if not kept:
        edits.append(Edit(statement.lineno, statement.end_lineno or statement.lineno, []))
        return 0
    names = ", ".join(alias.name if alias.asname is None else f"{alias.name} as {alias.asname}" for alias in kept)
    import_line = f"from {statement.module} import {names}\n"
    edits.append(Edit(statement.lineno, statement.end_lineno or statement.lineno, [import_line]))
    return len(kept)


def _import_lines(module: str, names: Sequence[str]) -> List[str]:
    """One import statement, split exactly as the generator splits a long one.

    A generated module path can leave no room for the imported name (128 characters
    before either name), so the statement is parenthesized and marked -- the same
    ``# noqa: E501`` the generator writes when it emits the import at all.
    """
    line = f"from {module} import {', '.join(names)}\n"
    if len(line) - 1 <= _LINE_LENGTH:
        return [line]
    return [f"from {module} import (  # noqa: E501\n", *(f"    {name},\n" for name in names), ")\n"]


def _swallow_blank_line(source: List[str], edits: List[Edit], before: int) -> None:
    """Take the blank line a deleted local import leaves behind with it."""
    if len(edits) == before or edits[-1].lines:
        return
    end = edits[-1].end
    if end < len(source) and not source[end].strip():
        edits[-1] = Edit(edits[-1].start, end + 1, [])


def _insert_imports(tree: ast.Module, hoisted: Set[Tuple[str, str]], edits: List[Edit]) -> None:
    """Add the hoisted imports to the module block, one line per module."""
    if not hoisted:
        return
    by_module: Dict[str, List[str]] = {}
    for module, name in sorted(hoisted):
        by_module.setdefault(module, []).append(name)
    lines = [line for module, names in by_module.items() for line in _import_lines(module, names)]
    last = max(
        (node.end_lineno or node.lineno for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))),
        default=0,
    )
    edits.append(Edit(last + 1, last, lines))


def check(paths: Sequence[pathlib.Path], sites: Sequence[Site]) -> Tuple[int, int]:
    """Report how many hoisted columns still answer ``declared_type(...) is None``."""
    from office365.runtime.converters.value import declared_type

    checked = missing = 0
    wanted = {(site.module, site.class_name, site.wire) for site in sites if site.wire}
    for path in paths:
        module_name = package_of(path)
        module = importlib.reload(importlib.import_module(module_name))
        for owner, class_name, wire in sorted(wanted):
            if owner != module_name:
                continue
            cls = getattr(module, class_name, None)
            checked += 1
            if cls is None or declared_type(cls, wire) is None:
                missing += 1
                print(f"{shown(path)}: {class_name}.{wire} still has no declared type", file=sys.stderr)
    return checked, missing


def shown(path: pathlib.Path) -> str:
    """Path as the reader of the report expects it: relative to the repository."""
    try:
        return str(path.relative_to(_ROOT))
    except ValueError:
        return str(path)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("root", nargs="?", default="office365", help="package directory to update (default: office365)")
    parser.add_argument("--only", action="append", choices=["enum", "value"], help="hoist only this kind of type")
    parser.add_argument("--dry-run", action="store_true", help="report the diff size without writing")
    parser.add_argument("--check", action="store_true", help="after writing, verify declared_type resolves")
    args = parser.parse_args(argv)

    only = set(args.only) if args.only else {"enum", "value"}
    graph = import_graph()
    paths = sorted(pathlib.Path(args.root).resolve().rglob("*.py"))
    hoisted = modules = 0
    written: List[pathlib.Path] = []
    all_sites: List[Site] = []
    for path in paths:
        candidates, skipped = plan_module(path, only)
        sites: List[Site] = []
        for site in candidates:
            if closes_a_cycle(graph, site.target, site.module):
                skipped.append(f"{site.class_name}.{site.getter} imports {site.name}: hoisting it would close a cycle")
                continue
            sites.append(site)
            graph.setdefault(site.module, set()).add(site.target)
        for reason in skipped:
            print(f"{shown(path)}: {reason}", file=sys.stderr)
        if not sites:
            continue
        hoisted += len({(site.target, site.name) for site in sites})
        modules += 1
        all_sites.extend(sites)
        if args.dry_run:
            print(f"{shown(path)}: {len(sites)}")
        else:
            apply(path, sites)
            written.append(path)
    print(f"{'would hoist' if args.dry_run else 'hoisted'}: {hoisted} imports in {modules} modules")
    if args.check and not args.dry_run:
        checked, missing = check(written, all_sites)
        print(f"declared_type: {checked - missing} of {checked} resolve, {missing} still None")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
