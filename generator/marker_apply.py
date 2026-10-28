"""Write the ``beta=`` markers a snapshot pair justifies into the model's source.

:mod:`generator.beta_markers` answers *what* every member should declare; this module
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

from generator.beta_markers import MarkerEdits, MemberMarker

#: ``, beta=True`` / ``, beta="otherName"`` / ``, beta=False`` -- with any spacing.
_BETA_ARGUMENT = re.compile(r",\s*beta=(?:True|False|\"[^\"]*\"|'[^']*')")
#: The ``name="..."`` argument, which is where a marker belongs (right after it).
_NAME_ARGUMENT = re.compile(r"(name=(?:\"[^\"]*\"|'[^']*'))")

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
            return "beta markers: model already declares every marker the snapshots justify"
        counts = ", ".join(f"{len(self.by_action(a))} {a}" for a in (ADDED, CHANGED, REMOVED))
        text = f"beta markers: {counts}"
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

    def path_of(self, type_name: str) -> Optional[Path]:
        for candidate in (self._by_odata.get(type_name), self.paths_for_class(_short(type_name))):
            if candidate and len(set(candidate)) == 1:
                return candidate[0]
        return None


def apply_markers(edits: MarkerEdits, files: TypeFiles, *, dry_run: bool = False) -> ApplyReport:
    """Bring the model's decorators in line with ``edits``, one decorator at a time."""
    report = ApplyReport(edits=[], skipped=[])
    rewrites: List[Tuple[Path, int, int, int, Optional[bool | str], MemberMarker, object]] = []
    for marker in edits.added + edits.changed:
        _collect(report, rewrites, files, marker, marker.beta)
    for marker in edits.removed:
        _collect(report, rewrites, files, marker, None)

    lines_of: Dict[Path, List[str]] = {}
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
    if not dry_run:
        for path, lines in lines_of.items():
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def _collect(
    report: ApplyReport,
    rewrites: List,
    files: TypeFiles,
    marker: MemberMarker,
    value: Optional[bool | str],
) -> None:
    """Queue one decorator rewrite, or record why it cannot be made."""
    if marker.kind == "method":
        report.skipped.append((marker, "methods are not generated (generate_methods is false)"))
        return
    located = _locate(files, marker)
    if located is None:
        report.skipped.append((marker, "no @odata(name=...) declares this member"))
        return
    path, lineno, start, end, declared = located
    rewrites.append((path, lineno, start, end, value, marker, declared))


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
