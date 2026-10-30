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

Two sources are repaired, not one. The getter's own import is the first; the second is a
name the annotation spells that only the module's ``if TYPE_CHECKING:`` block binds --
``Optional`` in a SharePoint model, ``timedelta`` in a booking one. Nothing there runs,
so the name is as unreachable as a local import and the answer is the same: put it in
the module block (``--only stdlib`` takes just the stdlib names).

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
from typing import Any, Dict, Iterator, List, NamedTuple, Optional, Sequence, Set, Tuple

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

_LINE_LENGTH = 121
KINDS = ("enum", "value", "stdlib")
_ROOT = pathlib.Path(__file__).resolve().parents[1]
_TARGET = _ROOT / "office365"


class Edit(NamedTuple):
    """A line range to replace (``end < start`` inserts before ``start``)."""

    start: int
    end: int
    lines: List[str]


class Site(NamedTuple):
    """One name a getter's annotation spells, and where the module hides it."""

    module: str
    target: str
    name: str
    class_name: str
    getter: str
    wire: Optional[str]
    kind: str
    source: str = "local"
    plain: bool = False


def key_of(site: Site) -> Tuple[str, str]:
    """What identifies a hoisted import: a name, or the whole module when it is one."""
    return (site.target, "" if site.plain else site.name)


def phrased(site: Site) -> str:
    """How the report names a site: a getter that imports the type, or only names it."""
    verb = "imports" if site.source == "local" else "annotates"
    return f"{site.class_name}.{site.getter} {verb} {site.name}"


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
    """``enum`` / ``value`` / ``entity`` / ``stdlib`` / ``other`` for the named type.

    ``stdlib`` is a type the module did not define -- ``Optional``, ``timedelta`` -- and
    such a name can never close an ``office365`` import cycle, so it needs no cycle gate.
    """
    from enum import Enum

    from office365.runtime.client_object import ClientObject
    from office365.runtime.client_value import ClientValue

    if target.split(".", maxsplit=1)[0] in ("typing", "typing_extensions"):
        return "stdlib"
    try:
        obj = getattr(importlib.import_module(target), name)
    except Exception:
        return None
    if not isinstance(obj, type):
        return "other"
    if (getattr(obj, "__module__", "") or "").split(".", maxsplit=1)[0] != "office365":
        # ``timedelta`` reached through a module that re-exports it is still stdlib.
        return "stdlib"
    for base, kind in ((Enum, "enum"), (ClientValue, "value"), (ClientObject, "entity")):
        if issubclass(obj, base):
            return kind
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


def module_bindings(tree: ast.Module) -> Dict[str, str]:
    """Names bound at module level, with the statement that binds them.

    ``TYPE_CHECKING`` blocks are excluded on purpose: they bind nothing when the
    module runs, so a name that lives only there is exactly what a hoist provides.
    """

    def walk(statements: Sequence[ast.stmt], found: Dict[str, str]) -> None:
        for node in statements:
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    found.setdefault(alias.asname or alias.name, f"from {node.module} import {alias.name}")
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    found.setdefault(alias.asname or alias.name.split(".")[0], f"import {alias.name}")
            elif isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                found.setdefault(node.name, f"{type(node).__name__} {node.name}")
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    for name in _target_names(target):
                        found.setdefault(name, "an assignment")
            elif isinstance(node, ast.AnnAssign):
                for name in _target_names(node.target):
                    found.setdefault(name, "an assignment")
            elif isinstance(node, ast.If):
                if isinstance(node.test, ast.Name) and node.test.id == "TYPE_CHECKING":
                    continue
                walk(node.body, found)
                walk(node.orelse, found)
            elif isinstance(node, (ast.Try, ast.With)):
                walk(node.body, found)

    found: Dict[str, str] = {}
    walk(tree.body, found)
    return found


def _target_names(target: ast.expr) -> Iterator[str]:
    if isinstance(target, ast.Name):
        yield target.id
    elif isinstance(target, (ast.Tuple, ast.List)):
        for item in target.elts:
            yield from _target_names(item)


def mentions(annotation: str, name: str) -> bool:
    """Whether the annotation text spells ``name`` as a word."""
    return re.search(rf"\b{re.escape(name)}\b", annotation) is not None


def type_checking_imports(block: Optional[ast.If]) -> Dict[str, Tuple[str, str, bool]]:
    """``local name -> (module, name, plain)`` for what the block binds.

    ``plain`` remembers ``import datetime`` against ``from datetime import datetime``:
    the two bind different objects under the same name, and both forms are in the tree.
    """
    found: Dict[str, Tuple[str, str, bool]] = {}
    if block is None:
        return found
    for statement in block.body:
        if isinstance(statement, ast.ImportFrom) and statement.module:
            for alias in statement.names:
                found.setdefault(alias.asname or alias.name, (statement.module, alias.name, False))
        elif isinstance(statement, ast.Import):
            for alias in statement.names:
                found.setdefault(alias.asname or alias.name.split(".")[0], (alias.name, alias.name, True))
    return found


def annotated_getters(tree: ast.Module) -> List[Tuple[ast.FunctionDef, str, Optional[str]]]:
    """Every property getter that states a return annotation, with its class."""
    found: List[Tuple[ast.FunctionDef, str, Optional[str]]] = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.FunctionDef) and is_property(node)):
            continue
        annotation = annotation_of(node)
        if annotation is not None:
            found.append((node, annotation, _enclosing_class(tree, node)))
    return found


def from_local_imports(
    module: str,
    bound: Dict[str, str],
    getters: Sequence[Tuple[ast.FunctionDef, str, Optional[str]]],
    only: Set[str],
) -> Tuple[List[Site], List[str]]:
    """Sites for the imports a getter states in its own body, and the ones to leave."""
    sites: List[Site] = []
    skipped: List[str] = []
    for node, annotation, parent in getters:
        for statement in local_imports(node):
            for alias in statement.names:
                if not mentions(annotation, alias.name):
                    continue
                where = f"{parent or module}.{node.name} imports {alias.name}"
                kind = kind_of(statement.module, alias.name)
                if kind is None:
                    skipped.append(f"{where} from an unimportable module {statement.module}")
                elif alias.name in bound:
                    # The module already binds the name, so the annotation resolves
                    # without the local copy -- but only to *that* binding: two models
                    # can share a simple name (``IdentitySet`` under ``directory`` and
                    # under ``directory.permissions``), and hoisting the getter's one
                    # would leave the annotation naming whichever import came second.
                    same = bound[alias.name] == f"from {statement.module} import {alias.name}"
                    skipped.append(
                        f"{where}: the module already binds {alias.name} "
                        f"({'the same import' if same else bound[alias.name]})"
                    )
                elif kind in only:
                    sites.append(
                        Site(module, statement.module, alias.name, parent or "", node.name, wire_name(node), kind)
                    )
    return sites, skipped


def from_type_checking(
    module: str,
    bound: Dict[str, str],
    getters: Sequence[Tuple[ast.FunctionDef, str, Optional[str]]],
    tree: ast.Module,
    only: Set[str],
) -> Tuple[List[Site], List[str]]:
    """Sites for the names only ``if TYPE_CHECKING:`` binds, and the ones to leave."""
    sites: List[Site] = []
    skipped: List[str] = []
    already_imported = {
        alias.name for node, _, _ in getters for statement in local_imports(node) for alias in statement.names
    }
    for local, (target, imported, plain) in sorted(type_checking_imports(type_checking_block(tree)).items()):
        if local in bound or local in already_imported:
            continue
        naming = [(node, parent) for node, annotation, parent in getters if mentions(annotation, local)]
        if not naming:
            continue
        kind = kind_of(target, imported)
        for node, parent in naming:
            where = f"{parent or module}.{node.name} annotates {local}"
            if kind is None:
                skipped.append(f"{where} from an unimportable module {target}")
            elif kind in only:
                sites.append(
                    Site(
                        module,
                        target,
                        imported,
                        parent or "",
                        node.name,
                        wire_name(node),
                        kind,
                        "type_checking",
                        plain,
                    )
                )
    return sites, skipped


def plan_module(path: pathlib.Path, only: Set[str] = frozenset(KINDS)) -> Tuple[List[Site], List[str]]:
    """Every name in ``path`` its getters reach for out of sight, and the ones it cannot move.

    Two places hide such a name: the getter's own body, and the module's
    ``if TYPE_CHECKING:`` block. The first is a site per getter; the second is a site
    per getter that *names* it, because the import is written once for the module and
    every annotation that spells it needs the same repair.
    """
    tree = ast.parse(path.read_text())
    if not has_future_annotations(tree):
        return [], []
    module = package_of(path)
    bound = module_bindings(tree)
    getters = annotated_getters(tree)
    sites, skipped = from_local_imports(module, bound, getters, only)
    more_sites, more_skipped = from_type_checking(module, bound, getters, tree, only)
    return sites + more_sites, skipped + more_skipped


def _enclosing_class(tree: ast.Module, target: ast.FunctionDef) -> Optional[str]:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and target in node.body:
            return node.name
    return None


def apply(path: pathlib.Path, sites: List[Site]) -> int:
    """Write the hoist for one module and return the number of imports it moved."""
    tree = ast.parse(path.read_text())
    source = path.read_text().splitlines(keepends=True)
    hoisted = {key_of(site) for site in sites}
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
    plan: List[Tuple[Any, List[ast.alias]]] = []
    remaining = 0
    for statement in block.body:
        if isinstance(statement, ast.ImportFrom) and statement.module:
            kept = [alias for alias in statement.names if (statement.module, alias.name) not in hoisted]
            remaining += len(kept)
            plan.append((statement, kept))
        elif isinstance(statement, ast.Import):
            kept = [alias for alias in statement.names if (alias.name, "") not in hoisted]
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
        if isinstance(statement, ast.Import):
            lines = [f"import {name}\n" for name in names]
        else:
            lines = _import_lines(statement.module, names)
        edits.append(Edit(statement.lineno, statement.end_lineno or statement.lineno, lines))


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
    lines: List[str] = []
    for module, names in by_module.items():
        plain = [name for name in names if not name]
        lines.extend(f"import {module}\n" for _ in plain)
        if len(plain) != len(names):
            lines.extend(_import_lines(module, [name for name in names if name]))
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
    parser.add_argument("--only", action="append", choices=KINDS, help="hoist only this kind of type")
    parser.add_argument("--dry-run", action="store_true", help="report the diff size without writing")
    parser.add_argument("--check", action="store_true", help="after writing, verify declared_type resolves")
    args = parser.parse_args(argv)

    only = set(args.only) if args.only else set(KINDS)
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
                skipped.append(f"{phrased(site)}: hoisting it would close a cycle")
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
