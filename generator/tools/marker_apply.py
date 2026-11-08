"""Write the ``beta=`` markers a snapshot pair justifies into the model's source.

:mod:`generator.tools.beta_markers` answers *what* every member should declare; this module
is the hand that types it, so extending the model and marking it are one operation
instead of two. Four properties make it safe to run on every generation:

* it edits the ``@odata(...)`` decorator of the member it names and nothing else -- the
  vocabulary the runtime already reads -- so a file no marker mentions is untouched;
* it is idempotent: a declaration that already says the wanted thing is left alone, so
  a second run over an up-to-date model is a no-op;
* it applies **removals**, which is the half that keeps the model honest over time. A
  member the next snapshot stops distinguishing -- a preview that went stable, a name
  the stable root adopted -- loses its marker rather than keeping a claim the metadata
  no longer makes;
* it reports what it could not resolve instead of guessing, because a marker written
  onto the wrong member reads as authoritative.

Resolution is by the type's own ``entity_type_name`` (authoritative, no imports), then
by class name, then up the declared base chain -- a member may be declared on a base
class, and then the marker has to go into *that* class's file.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from generator.build.naming import to_snake_case
from generator.tools.beta_markers import STABLE_ONLY, MarkerEdits, MemberMarker, VersionMarker

#: ``, beta=True`` / ``, beta="otherName"`` / ``, beta=False`` -- with any spacing.
_BETA_ARGUMENT = re.compile(r",\s*beta=(?:True|False|\"[^\"]*\"|'[^']*')")
#: The ``name="..."`` argument, which is where a marker belongs (right after it).
_NAME_ARGUMENT = re.compile(r"(name=(?:\"[^\"]*\"|'[^']*'))")

#: The declaration module, whose import a gated class extends by one name.
DECLARATION_MODULE = "office365.runtime.types.odata_property"
_DECLARATION_IMPORT = re.compile(rf"^from {re.escape(DECLARATION_MODULE)} import ([^()\n]+)$")

#: The member name a type-level gate reports under: the decorator, not its storage.
VERSION = "version"

#: The same, for the identity a type declares above the class.
KEY = "key"

#: The decorator a member's wire name is declared with.
ODATA = "odata"

ADDED = "added"
CHANGED = "changed"
REMOVED = "removed"


@dataclass(frozen=True)
class AppliedEdit:
    """One decorator rewritten, with enough context to read as a diff."""

    path: str
    type_name: str
    member: str
    action: str
    before: str
    after: str

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "type": self.type_name,
            "member": self.member,
            "action": self.action,
            "before": self.before,
            "after": self.after,
        }


@dataclass
class ApplyReport:
    """What the pass wrote, and what it could not write."""

    edits: List[AppliedEdit]
    skipped: List[Tuple[MemberMarker, str]]
    #: What the pass calls itself in a one-line summary; the same shape writes the
    #: ``beta=`` markers and the ``@key`` declarations.
    label: str = "beta markers"

    @property
    def is_empty(self) -> bool:
        return not (self.edits or self.skipped)

    def by_action(self, action: str) -> List[AppliedEdit]:
        return [edit for edit in self.edits if edit.action == action]

    def to_dict(self) -> dict:
        return {
            "count": len(self.edits),
            "applied": [edit.to_dict() for edit in self.edits],
            "skipped": [dict(marker.to_dict(), reason=reason) for marker, reason in self.skipped],
        }

    def render(self) -> str:
        if self.is_empty:
            return f"{self.label}: model already declares every marker the snapshots justify"
        counts = ", ".join(f"{len(self.by_action(a))} {a}" for a in (ADDED, CHANGED, REMOVED))
        text = f"{self.label}: {counts}"
        if self.skipped:
            text += f", {len(self.skipped)} unresolved"
        return text


class TypeFiles:
    """The model tree, indexed by ``entity_type_name`` and by class name.

    Pure AST: no module is imported, so a tree that does not import cleanly yet is
    still markable.
    """

    def __init__(self, root: Path) -> None:
        self.root = root
        self._by_odata: Dict[str, List[Path]] = {}
        self._by_class: Dict[str, List[Path]] = {}
        self._trees: Dict[Path, ast.Module] = {}
        for path in sorted(root.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            self._trees[path] = tree
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    self._by_class.setdefault(node.name, []).append(path)
                    name = _entity_type_name(node)
                    if name:
                        self._by_odata.setdefault(name, []).append(path)

    def tree(self, path: Path) -> ast.Module:
        return self._trees[path]

    def paths_for_class(self, class_name: str) -> List[Path]:
        return self._by_class.get(class_name, [])

    def class_for(self, type_name: str) -> Optional[Tuple[Path, ast.ClassDef]]:
        """The class that *is* ``type_name`` -- never a same-named type from another waypoint.

        ``path_of`` falls back to the class name, which is right for finding the decorator
        a member belongs to and wrong here: ``microsoft.graph.UserConfiguration`` and
        ``microsoft.graph.industryData.UserConfiguration`` share a short name, so a gate
        for the one that was never generated would land on the other one's file.
        """
        path = self.path_of(type_name)
        if path is None:
            return None
        short = _short(type_name)
        for node in ast.walk(self.tree(path)):
            if not isinstance(node, ast.ClassDef):
                continue
            declared = _entity_type_name(node)
            if declared == type_name or (declared is None and node.name == short):
                return path, node
        return None

    def declaring(self, name: str) -> List[Tuple[Path, ast.ClassDef]]:
        """Every class in the tree that carries ``@<name>(...)``, whatever its type name."""
        found: List[Tuple[Path, ast.ClassDef]] = []
        for path, tree in self._trees.items():
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and decorator_line(node, name) is not None:
                    found.append((path, node))
        return found

    def class_chain(self, type_name: str) -> List[Tuple[Path, ast.ClassDef]]:
        """The class that declares ``type_name`` and its declared bases, nearest first.

        A fact can be stated anywhere on the chain, and which class states it decides the
        file it belongs in: a member declared on a base class is marked in *that* class.
        """
        located = self.class_for(type_name)
        if located is None:
            return []
        return [located, *_bases(self, type_name)]

    def is_addressed(self, type_name: str) -> bool:
        """Whether a request can name the type, which is the only thing a gate can refuse."""
        located = self.class_for(type_name)
        return located is not None and _is_addressed(self, located[1], type_name)

    def path_of(self, type_name: str) -> Optional[Path]:
        for candidate in (self._by_odata.get(type_name), self.paths_for_class(_short(type_name))):
            if candidate and len(set(candidate)) == 1:
                return candidate[0]
        return None


def apply_markers(edits: MarkerEdits, files: TypeFiles, *, dry_run: bool = False) -> ApplyReport:
    """Bring the model's decorators in line with ``edits``, one decorator at a time."""
    report = ApplyReport(edits=[], skipped=[])
    rewrites: List[Tuple[Path, int, int, int, Optional[bool | str], MemberMarker, object]] = []
    ops: List[Tuple[Path, int, int, List[str]]] = []
    lines_of: Dict[Path, List[str]] = {}
    for marker in edits.added + edits.changed:
        _collect(report, rewrites, ops, lines_of, files, marker, marker.beta)
    for marker in edits.removed:
        _collect(report, rewrites, ops, lines_of, files, marker, None)

    for marker in edits.types_added:
        _queue_version(report, files, ops, lines_of, marker)
    for marker in edits.types_removed:
        _queue_ungate(report, files, ops, lines_of, marker)

    for path, lineno, start, end, value, marker, declared in rewrites:
        lines = lines_of.setdefault(path, path.read_text(encoding="utf-8").splitlines())
        line = lines[lineno]
        span_start, span_end = _with_decorator_sign(line, start, end)
        before = line[span_start:span_end]
        after = _rewrite(before, value)
        if before == after:
            continue
        if value is None:
            action = REMOVED
        else:
            action = CHANGED if declared is not None else ADDED
        lines[lineno] = line[:span_start] + after + line[span_end:]
        report.edits.append(
            AppliedEdit(
                path=str(path),
                type_name=marker.type_name,
                member=marker.member,
                action=action,
                before=before,
                after=after,
            )
        )
    _flush(lines_of, ops, dry_run=dry_run)
    return report


def apply_keys(plan, files: TypeFiles, *, dry_run: bool = False) -> ApplyReport:
    """Write the ``@key(...)`` declarations ``plan`` justifies, and remove the rest.

    The plan decides *what* is true; this decides nothing and writes it -- the same split
    ``apply_markers`` keeps with :mod:`generator.tools.beta_markers`. The removal half is what
    keeps the tree honest: a key the next snapshot stops stating, or starts stating as the
    family default, must not stay on the class claiming a rule nobody derives any more.
    """
    skipped = [
        (MemberMarker(marker.type_name, KEY, "", marker.key, STABLE_ONLY), reason) for marker, reason in plan.skipped
    ]
    report = ApplyReport(edits=[], skipped=skipped, label="keys")
    ops: List[Tuple[Path, int, int, List[str]]] = []
    lines_of: Dict[Path, List[str]] = {}
    kept = set()
    for marker in plan.markers:
        located = files.class_for(marker.type_name)
        if located is not None:
            kept.add((located[0], located[1].name))
        _queue_key(report, files, ops, lines_of, marker)
    for path, class_node in files.declaring(KEY):
        if (path, class_node.name) not in kept:
            _queue_unkey(report, ops, lines_of, path, class_node)
    _flush(lines_of, ops, dry_run=dry_run)
    return report


def _flush(lines_of: Dict[Path, List[str]], ops: List[Tuple[Path, int, int, List[str]]], *, dry_run: bool) -> None:
    """Apply the queued operations bottom-up, then write the files that changed.

    Every queued operation indexes the file as it was read, so they run after the
    one-line rewrites (which never change a line count) and from the bottom up: an edit
    never moves a line the loop has not reached yet. A decorator and a class that lost
    one can sit in the same file, so insertions and deletions share one ordering.
    """
    for path, start, end, replacement in sorted(ops, key=lambda op: (str(op[0]), -op[1])):
        lines_of[path][start:end] = replacement
    if not dry_run:
        for path, lines in lines_of.items():
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _queue_key(
    report: ApplyReport,
    files: TypeFiles,
    ops: List[Tuple[Path, int, int, List[str]]],
    lines_of: Dict[Path, List[str]],
    marker,
) -> None:
    """Declare ``@key(...)`` above the class ``marker`` names, or say it is already right."""
    located = files.class_for(marker.type_name)
    if located is None:
        report.skipped.append(
            (MemberMarker(marker.type_name, KEY, "", marker.key, STABLE_ONLY), "no class declares this type")
        )
        return
    path, class_node = located
    lines = lines_of.setdefault(path, path.read_text(encoding="utf-8").splitlines())
    wanted = _key_decorator(marker)
    declared_at = decorator_line(class_node, KEY)
    if declared_at is not None:
        before = lines[declared_at]
        if before.strip() == wanted:
            return
        ops.append((path, declared_at, declared_at + 1, [wanted]))
        action = CHANGED
    else:
        at = _below_decorators(class_node)
        ops.append((path, at, at, [wanted]))
        before = ""
        action = ADDED
    _declare_import(ops, path, lines, KEY)
    report.edits.append(
        AppliedEdit(
            path=str(path),
            type_name=marker.type_name,
            member=KEY,
            action=action,
            before=before,
            after=wanted,
        )
    )


def _queue_unkey(
    report: ApplyReport,
    ops: List[Tuple[Path, int, int, List[str]]],
    lines_of: Dict[Path, List[str]],
    path: Path,
    class_node: ast.ClassDef,
) -> None:
    """Remove a ``@key(...)`` the snapshot stops justifying, and its import with it."""
    declared_at = decorator_line(class_node, KEY)
    if declared_at is None:
        return
    lines = lines_of.setdefault(path, path.read_text(encoding="utf-8").splitlines())
    before = lines[declared_at]
    ops.append((path, declared_at, declared_at + 1, []))
    if not any(line.lstrip().startswith("@key(") for index, line in enumerate(lines) if index != declared_at):
        _drop_import(ops, path, lines, KEY)
    report.edits.append(
        AppliedEdit(
            path=str(path),
            type_name=_entity_type_name(class_node) or class_node.name,
            member=KEY,
            action=REMOVED,
            before=before,
            after="",
        )
    )


def _queue_version(
    report: ApplyReport,
    files: TypeFiles,
    ops: List[Tuple[Path, int, int, List[str]]],
    lines_of: Dict[Path, List[str]],
    marker: VersionMarker,
) -> None:
    """Declare ``@version(...)`` above the class ``marker`` names, or say it is already right."""
    located = files.class_for(marker.type_name)
    if located is None:
        report.skipped.append(
            (MemberMarker(marker.type_name, VERSION, "", marker.version, STABLE_ONLY), "no class declares this type")
        )
        return
    path, class_node = located
    lines = lines_of.setdefault(path, path.read_text(encoding="utf-8").splitlines())
    if not _is_addressed(files, class_node, marker.type_name):
        # Nothing would enforce it: a complex value or an enum is never the entity a
        # request names, so a gate there is a comment pretending to be a rule.
        if _version_line(class_node) is not None:
            _queue_ungate(report, files, ops, lines_of, marker)
        else:
            report.skipped.append(
                (
                    MemberMarker(marker.type_name, VERSION, "", marker.version, STABLE_ONLY),
                    "a complex or enum type is not addressed by a request",
                )
            )
        return
    wanted = _version_decorator(marker)
    declared_at = _version_line(class_node)
    if declared_at is not None:
        before = lines[declared_at]
        if before.strip() == wanted:
            return
        ops.append((path, declared_at, declared_at + 1, [wanted]))
        action = CHANGED
    else:
        after = _decorator_start(class_node)
        if any(queued[0] == path and queued[1] == after for queued in ops):
            return
        ops.append((path, after, after, [wanted]))
        # A gate written by an older spelling as a body statement would still be there,
        # shadowed by the decorator and read by nobody: the pass takes its own litter out.
        stale = _version_statement(class_node)
        if stale is not None:
            # The declaration was the class body's first line, so the blank line after it
            # goes too -- otherwise the body starts with an empty line.
            stop = stale[1] + 1 if stale[1] < len(lines) and not lines[stale[1]].strip() else stale[1]
            ops.append((path, stale[0], stop, []))
        before = ""
        action = ADDED
    _declare_import(ops, path, lines)
    report.edits.append(
        AppliedEdit(
            path=str(path),
            type_name=marker.type_name,
            member=VERSION,
            action=action,
            before=before,
            after=wanted,
        )
    )


def _queue_ungate(
    report: ApplyReport,
    files: TypeFiles,
    ops: List[Tuple[Path, int, int, List[str]]],
    lines_of: Dict[Path, List[str]],
    marker: VersionMarker,
) -> None:
    """Remove an ``@version(...)`` the snapshots stop justifying, and its import with it."""
    located = files.class_for(marker.type_name)
    if located is None:
        return
    path, class_node = located
    declared_at = _version_line(class_node)
    if declared_at is None:
        return
    lines = lines_of.setdefault(path, path.read_text(encoding="utf-8").splitlines())
    before = lines[declared_at]
    ops.append((path, declared_at, declared_at + 1, []))
    if not any(line.lstrip().startswith("@version(") for index, line in enumerate(lines) if index != declared_at):
        _drop_import(ops, path, lines)
    report.edits.append(
        AppliedEdit(
            path=str(path),
            type_name=marker.type_name,
            member=VERSION,
            action=REMOVED,
            before=before,
            after="",
        )
    )


def decorator_line(class_node: ast.ClassDef, name: str) -> Optional[int]:
    """The 0-based line the class's ``@<name>(...)`` decorator occupies."""
    for decorator in class_node.decorator_list:
        if isinstance(decorator, ast.Call) and getattr(decorator.func, "id", None) == name:
            return decorator.lineno - 1
    return None


def _version_line(class_node: ast.ClassDef) -> Optional[int]:
    """The 0-based line the class's ``@version(...)`` decorator occupies."""
    return decorator_line(class_node, VERSION)


def _decorator_start(class_node: ast.ClassDef) -> int:
    """The 0-based line the class's decorators start on -- above all of them, not below."""
    return min([decorator.lineno for decorator in class_node.decorator_list] + [class_node.lineno]) - 1


def _version_statement(class_node: ast.ClassDef) -> Optional[Tuple[int, int]]:
    """The span of a body ``_versions = ...`` an older spelling left behind."""
    for node in class_node.body:
        if isinstance(node, ast.Assign):
            targets = [target.id for target in node.targets if isinstance(target, ast.Name)]
            if targets == ["_versions"] and node.end_lineno is not None:
                return node.lineno - 1, node.end_lineno
    return None


def _declare_import(
    ops: List[Tuple[Path, int, int, List[str]]], path: Path, lines: List[str], name: str = VERSION
) -> None:
    """Add ``name`` to the declaration-module import the generated file already spells."""
    for index, line in enumerate(lines):
        match = _DECLARATION_IMPORT.match(line.strip())
        if match is None:
            continue
        names = [declared.strip() for declared in match.group(1).split(",")]
        pending = [queued[3][0] for queued in ops if queued[0] == path and queued[1] == index and queued[3]]
        if name in names or any(name in line for line in pending):
            return
        written = ", ".join(sorted({*names, name}))
        ops.append((path, index, index + 1, [f"from {DECLARATION_MODULE} import {written}"]))
        return
    _insert_import(ops, path, lines, name)


def _insert_import(
    ops: List[Tuple[Path, int, int, List[str]]], path: Path, lines: List[str], name: str = VERSION
) -> None:
    """Write the import whole, for a class the template gave no other declaration."""
    statement = f"from {DECLARATION_MODULE} import {name}"
    candidates = [index for index, line in enumerate(lines) if line.startswith("from office365")]
    before = [index for index in candidates if lines[index] > statement]
    at = before[0] if before else (candidates[-1] + 1 if candidates else 0)
    ops.append((path, at, at, [statement]))


def _drop_import(ops: List[Tuple[Path, int, int, List[str]]], path: Path, lines: List[str], name: str = VERSION) -> None:
    """Take ``name`` back out, so an import nothing names does not outlive the declaration."""
    for index, line in enumerate(lines):
        match = _DECLARATION_IMPORT.match(line.strip())
        if match is None:
            continue
        names = [declared.strip() for declared in match.group(1).split(",")]
        if name not in names:
            return
        kept = [declared for declared in names if declared != name]
        if not kept:
            ops.append((path, index, index + 1, []))
            return
        ops.append((path, index, index + 1, [f"from {DECLARATION_MODULE} import {', '.join(kept)}"]))
        return


#: The two bases a value is seeded with: a value is declared last, under a name no
#: request names, so nothing a gate states about addressing applies to it.
VALUE_BASES = frozenset({"ClientValue", "ComplexType"})


def _declared_bases(node: ast.ClassDef) -> set[str]:
    """The base names ``node`` states, as written (the import makes them short)."""
    return {getattr(base, "id", None) or getattr(base, "attr", None) or "" for base in node.bases}


def _is_addressed(files: "TypeFiles", class_node: ast.ClassDef, type_name: str) -> bool:
    """Whether a request can name the type -- which is the only thing a gate can refuse.

    A value is recognised by its base, not by a decorator. It used to carry one, so a
    source-level decorator was also a fact about the kind; the base class applies
    ``dataclass`` now, and a value's kind is the base it was seeded with.
    """
    declared = _declared_bases(class_node)
    if "Enum" in declared or declared & VALUE_BASES:
        return False
    return not any(node.name in VALUE_BASES for _, node in _bases(files, type_name))


def _below_decorators(class_node: ast.ClassDef) -> int:
    """The 0-based line the ``class`` statement begins on: under every decorator it has.

    A type's facts stack outwards -- ``@version`` refuses a request before ``@key`` decides
    an address -- so a new one is written closest to the class, where a reader meets it
    last and in the same place a hand-written file puts it.
    """
    return class_node.lineno - 1


def _key_decorator(marker) -> str:
    """The decorator, as source: the wire name of the key property, quoted."""
    return f"@key({json.dumps(marker.key)})"


def _version_decorator(marker: VersionMarker) -> str:
    """The decorator, as source: one root per argument, in a stable order."""
    roots = ", ".join(json.dumps(root) for root in sorted({marker.version}))
    return f"@version({roots})"


def _collect(
    report: ApplyReport,
    rewrites: List,
    ops: List,
    lines_of: Dict[Path, List[str]],
    files: TypeFiles,
    marker: MemberMarker,
    value: Optional[bool | str],
) -> None:
    """Queue one decorator rewrite, or record why it cannot be made."""
    if marker.kind == "method":
        _collect_method(report, ops, lines_of, files, marker, value)
        return
    located = _locate(files, marker)
    if located is None:
        report.skipped.append((marker, "no @odata(name=...) declares this member"))
        return
    path, lineno, start, end, declared = located
    rewrites.append((path, lineno, start, end, value, marker, declared))


def _collect_method(
    report: ApplyReport,
    ops: List,
    lines_of: Dict[Path, List[str]],
    files: TypeFiles,
    marker: MemberMarker,
    value: Optional[bool | str],
) -> None:
    """Declare an operation, which has no ``@odata`` of its own to extend.

    A property's gate is written into the declaration its getter already carries; an
    operation carries none, because a method's OData name was, until now, only the string
    its query was built with -- which is exactly the argument for declaring it here. The
    row a request reads is a name and a version, and the query asks the schema the same
    question a projection asks: does this root declare this name?

    ``selectable=False`` keeps the operation out of ``$select``: it is a member of the
    type, not a column of its resource.
    """
    located = _method_for(files, marker)
    if located is None:
        report.skipped.append((marker, "no method of that name is generated"))
        return
    path, function = located
    lines = lines_of.setdefault(path, path.read_text(encoding="utf-8").splitlines())
    declared_at = _method_decorator_line(function)
    if value is None:
        # The snapshots stop justifying the gate: the declaration goes whole, because an
        # operation the two roots agree about has nothing to say about which one it is.
        if declared_at is None:
            return
        before = lines[declared_at]
        ops.append((path, declared_at, declared_at + 1, []))
        _drop_import(ops, path, lines, name=ODATA)
        report.edits.append(
            AppliedEdit(
                path=str(path),
                type_name=marker.type_name,
                member=marker.member,
                action=REMOVED,
                before=before,
                after="",
            )
        )
        return
    wanted = _method_decorator(marker.member, value)
    if declared_at is None:
        # Directly above the ``def``, below whatever else decorates it -- where a getter
        # says its own name, and the last thing a reader meets before the signature.
        at = function.decorator_list[0].lineno - 1 if function.decorator_list else function.lineno - 1
        ops.append((path, at, at, [" " * function.col_offset + wanted]))
        action = ADDED
        before = ""
    else:
        before = lines[declared_at]
        ops.append((path, declared_at, declared_at + 1, [" " * function.col_offset + wanted]))
        action = CHANGED if before.strip() != wanted else None
        if action is None:
            return
    _declare_import(ops, path, lines, name=ODATA)
    report.edits.append(
        AppliedEdit(
            path=str(path),
            type_name=marker.type_name,
            member=marker.member,
            action=action,
            before=before,
            after=wanted,
        )
    )


def _method_for(files: TypeFiles, marker: MemberMarker) -> Optional[Tuple[Path, ast.FunctionDef]]:
    """The generated ``def`` that submits ``marker``'s operation, on the chain."""
    python_name = to_snake_case(marker.member)
    for path, class_node in files.class_chain(marker.type_name):
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef) and node.name == python_name:
                return path, node
    return None


def _method_decorator_line(function: ast.FunctionDef) -> Optional[int]:
    """The 0-based line of an ``@odata(...)`` already above ``function``, if any."""
    for decorator in function.decorator_list:
        if isinstance(decorator, ast.Call) and getattr(decorator.func, "id", None) == ODATA:
            return decorator.lineno - 1
    return None


def _method_decorator(member: str, value: Optional[bool | str]) -> str:
    """The declaration an operation carries: its wire name, one root, and no column."""
    literal = "True" if value is True else "False" if value is False else json.dumps(value)
    return f"@odata(name={json.dumps(member)}, beta={literal}, selectable=False)"


def _locate(files: TypeFiles, marker: MemberMarker) -> Optional[Tuple[Path, int, int, int, object]]:
    """Where ``marker``'s ``@odata`` decorator is: file, line index, span, current value."""
    own = files.path_of(marker.type_name)
    if own is not None:
        for class_node in _classes_for(files.tree(own), marker.type_name):
            found = _decorator_in(class_node, marker.member)
            if found is not None:
                return (own, *found)
    for path, class_node in _bases(files, marker.type_name):
        found = _decorator_in(class_node, marker.member)
        if found is not None:
            return (path, *found)
    return None


def _bases(files: TypeFiles, type_name: str) -> Iterable[Tuple[Path, ast.ClassDef]]:
    """The base classes of ``type_name``, breadth first, following the declared bases."""
    seen: set[str] = set()
    queue: List[str] = [_short(type_name)]
    while queue:
        current = queue.pop(0)
        for path in set(files.paths_for_class(current)):
            for node in files.tree(path).body:
                if not isinstance(node, ast.ClassDef) or node.name != current:
                    continue
                for base in node.bases:
                    name = getattr(base, "id", None) or getattr(base, "attr", None)
                    if not name or name in seen:
                        continue
                    seen.add(name)
                    queue.append(name)
                    for base_path in set(files.paths_for_class(name)):
                        for candidate in files.tree(base_path).body:
                            if isinstance(candidate, ast.ClassDef) and candidate.name == name:
                                yield base_path, candidate


def _classes_for(tree: ast.Module, type_name: str) -> Iterable[ast.ClassDef]:
    short = _short(type_name)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and (_entity_type_name(node) == type_name or node.name == short):
            yield node


def _decorator_in(class_node: ast.ClassDef, member: str) -> Optional[Tuple[int, int, int, object]]:
    """The ``@odata`` of ``member``: line index, span, and the value it carries now."""
    for node in class_node.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call) or getattr(decorator.func, "id", None) != "odata":
                continue
            keywords = {keyword.arg: keyword.value for keyword in decorator.keywords if keyword.arg}
            name = keywords.get("name")
            if not (isinstance(name, ast.Constant) and name.value == member):
                continue
            if decorator.lineno != decorator.end_lineno:
                return None
            end = decorator.end_col_offset if decorator.end_col_offset is not None else decorator.col_offset
            return (decorator.lineno - 1, decorator.col_offset, end, _value(keywords.get("beta")))
    return None


def _rewrite(segment: str, value: Optional[object]) -> str:
    """``@odata(name="x", ...)`` with ``beta`` set to ``value`` (dropped when ``None``)."""
    stripped = _BETA_ARGUMENT.sub("", segment)
    if value is None:
        return stripped
    literal = ("True" if value else "False") if isinstance(value, bool) else json.dumps(value)
    return _NAME_ARGUMENT.sub(rf"\1, beta={literal}", stripped, count=1)


def _with_decorator_sign(line: str, start: int, end: int) -> Tuple[int, int]:
    """Widen the span to the ``@`` so a report reads like the source it changed."""
    return (start - 1, end) if start and line[start - 1] == "@" else (start, end)


def _value(node: Optional[ast.expr]) -> object:
    if isinstance(node, ast.Constant) and isinstance(node.value, (bool, str)):
        return node.value
    return None


def _entity_type_name(node: ast.ClassDef) -> Optional[str]:
    for child in node.body:
        if isinstance(child, ast.FunctionDef) and child.name == "entity_type_name":
            for statement in ast.walk(child):
                if isinstance(statement, ast.Return) and isinstance(statement.value, ast.Constant):
                    if isinstance(statement.value.value, str):
                        return statement.value.value
    return None


def _short(type_name: str) -> str:
    return type_name.rsplit(".", 1)[-1]
