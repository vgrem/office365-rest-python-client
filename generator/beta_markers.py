"""What the ``beta=`` markers should say, and how to bring a model up to that.

A marker is derived, never asserted: the two metadata snapshots are the only source of
truth, so the desired state is a pure function of :func:`generator.metadata_diff.diff_metadata`
and nothing about it is stored. That is what makes the third operation possible -- a
marker that the *next* snapshot stops justifying has to be **deleted**, not left behind.
Beta drops members, adopts the stable spelling, and re-announces previews as stable;
each of those turns an existing ``beta=True`` or ``beta="otherName"`` into noise a
reader would trust and a request would send.

So a run has three inputs, not two: the base snapshot, the target snapshot, and what
the model currently declares (read back from the model's own source, since the code is
the state). The difference between desired and declared is the edit list: add, change,
remove.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Tuple, Union

from office365.runtime.types.odata_property import PREVIEW

from generator.metadata_diff import METHOD, NAVIGATION, PROPERTY, MetadataDelta

#: Marker value: only the target (preview) root declares this member.
BETA_ONLY = "beta-only"
#: Marker value: both roots declare it, the target spells it differently.
RENAMED = "renamed"
#: Marker value: only the base root declares it; the target dropped it.
STABLE_ONLY = "stable-only"

#: What a declaration holds: ``None`` for "no marker", a bool, or the target's spelling.
MarkerValue = Union[bool, str, None]


@dataclass(frozen=True)
class MemberMarker:
    """One ``beta=`` argument a declaration needs, and why it needs it."""

    type_name: str
    member: str
    kind: str
    beta: MarkerValue
    reason: str

    @property
    def key(self) -> Tuple[str, str]:
        return self.type_name, self.member

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "member": self.member,
            "kind": self.kind,
            "beta": self.beta,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class VersionMarker:
    """A type only one service root declares, as a fact to state on the class itself.

    A member marker says "this attribute is the preview root's"; this one says "the type
    is". They are separate answers because they fail separately: a stable client that
    selects a preview member is refused by the projection, while a stable client that
    builds a preview-only *class* asks its root for an entity the root has no schema for.
    """

    type_name: str
    version: str

    def to_dict(self) -> dict:
        return {"type": self.type_name, "version": self.version}


@dataclass
class MarkerPlan:
    """Every marker the target snapshot justifies, across the whole model."""

    base: str
    target: str
    markers: List[MemberMarker]
    types: Tuple[VersionMarker, ...] = ()

    def by_reason(self, reason: str) -> List[MemberMarker]:
        return [marker for marker in self.markers if marker.reason == reason]

    def restricted(self, types: Iterable[str]) -> "MarkerPlan":
        """The part of the plan that lands on ``types`` (short or qualified names).

        A whole-tree plan is the honest default, but a first pass onto a handful of
        types is how the machinery earns trust: the plan is still derived from the
        snapshots, only its reach is narrowed.
        """
        wanted = {name.rsplit(".", 1)[-1].lower() for name in types}
        return MarkerPlan(
            base=self.base,
            target=self.target,
            markers=[marker for marker in self.markers if marker.type_name.rsplit(".", 1)[-1].lower() in wanted],
            types=tuple(marker for marker in self.types if marker.type_name.rsplit(".", 1)[-1].lower() in wanted),
        )

    def to_dict(self) -> dict:
        return {
            "metadata": {"base": self.base, "target": self.target},
            "count": len(self.markers),
            "markers": [marker.to_dict() for marker in self.markers],
            "count_types": len(self.types),
            "types": [marker.to_dict() for marker in self.types],
        }

    def render(self) -> str:
        counts = {reason: len(self.by_reason(reason)) for reason in (BETA_ONLY, RENAMED, STABLE_ONLY)}
        text = (
            f"{self.target} markers: {len(self.markers)} total -- "
            f"{counts[BETA_ONLY]} beta-only, {counts[RENAMED]} renamed, {counts[STABLE_ONLY]} stable-only"
        )
        if self.types:
            text += f"; {len(self.types)} type(s) the target alone declares"
        return text


@dataclass
class MarkerEdits:
    """What a model has to do to carry exactly the markers its snapshots justify."""

    added: List[MemberMarker]
    changed: List[MemberMarker]
    removed: List[MemberMarker]
    types_added: List[VersionMarker] = field(default_factory=list)
    types_removed: List[VersionMarker] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not (self.added or self.changed or self.removed or self.types_added or self.types_removed)

    @property
    def count(self) -> int:
        return len(self.added) + len(self.changed) + len(self.removed) + len(self.types_added) + len(self.types_removed)

    def to_dict(self) -> dict:
        return {
            "count": self.count,
            "added": [marker.to_dict() for marker in self.added],
            "changed": [marker.to_dict() for marker in self.changed],
            "removed": [marker.to_dict() for marker in self.removed],
            "types_added": [marker.to_dict() for marker in self.types_added],
            "types_removed": [marker.to_dict() for marker in self.types_removed],
        }

    def render(self) -> str:
        if self.is_empty:
            return "beta markers: up to date"
        text = f"beta markers: {len(self.added)} to add, {len(self.changed)} to change, {len(self.removed)} to remove"
        if self.types_added or self.types_removed:
            text += f"; {len(self.types_added)} type(s) to gate, {len(self.types_removed)} to ungate"
        return text


def plan_markers(delta: MetadataDelta) -> MarkerPlan:
    """The marker every member of ``delta`` justifies, and nothing else."""
    markers: List[MemberMarker] = []
    for reason, kind, bucket in (
        (BETA_ONLY, PROPERTY, delta.properties_only_in_target),
        (BETA_ONLY, NAVIGATION, delta.navigations_only_in_target),
        (BETA_ONLY, METHOD, delta.methods_only_in_target),
        (STABLE_ONLY, PROPERTY, delta.properties_only_in_base),
        (STABLE_ONLY, NAVIGATION, delta.navigations_only_in_base),
    ):
        markers.extend(_flatten(bucket, kind, True if reason == BETA_ONLY else False, reason))
    markers.extend(
        MemberMarker(rename.type_name, rename.base, rename.kind, rename.target, RENAMED) for rename in delta.renamed
    )
    markers.sort(key=lambda marker: (marker.type_name, marker.kind, marker.member))
    return MarkerPlan(
        base=delta.base,
        target=delta.target,
        markers=markers,
        types=tuple(VersionMarker(name, PREVIEW) for name in sorted(delta.types_only_in_target)),
    )


def compare_markers(
    plan: MarkerPlan,
    declared: Mapping[Tuple[str, str], MarkerValue],
    declared_versions: Optional[Mapping[str, Iterable[str]]] = None,
) -> MarkerEdits:
    """Diff the plan against what the model declares now: add, change, remove.

    ``declared`` is keyed by ``(type name, member)`` and holds the marker the source
    currently carries -- ``True``, ``False``, the target spelling, or (absent) nothing.
    A marker the model declares and the plan does not justify is reported for removal:
    that is how a preview that went stable, or a member the preview root dropped, stops
    being marked.
    """
    edits = MarkerEdits(added=[], changed=[], removed=[])
    wanted = {marker.key: marker for marker in plan.markers}
    for marker in plan.markers:
        if marker.key not in declared:
            edits.added.append(marker)
        elif declared[marker.key] != marker.beta:
            edits.changed.append(marker)
    for key, value in declared.items():
        if key in wanted:
            continue
        type_name, member = key
        edits.removed.append(MemberMarker(type_name, member, "", value, STABLE_ONLY))
    edits.removed.sort(key=lambda marker: marker.key)

    # The type-level fact is compared the same way: whatever the class states now must be
    # what the plan says, and a gate the snapshots no longer justify is removed.
    has_versions = declared_versions if declared_versions is not None else {}
    wanted_types = {marker.type_name: marker for marker in plan.types}
    for marker in plan.types:
        current = frozenset(has_versions.get(marker.type_name, ()))
        if current != frozenset({marker.version}):
            edits.types_added.append(marker)
    for type_name, versions in has_versions.items():
        if type_name not in wanted_types and frozenset(versions):
            edits.types_removed.append(VersionMarker(type_name, PREVIEW))
    edits.types_removed.sort(key=lambda marker: marker.type_name)
    return edits


def read_declared_markers(sources: Mapping[str, Union[str, Path]]) -> Dict[Tuple[str, str], MarkerValue]:
    """Read the markers a model file already declares, keyed by ``(type, member)``.

    The generator knows which CSDL type each file holds, so the type name is the
    caller's, not something guessed from the source; only the decorators are read.
    """
    declared: Dict[Tuple[str, str], MarkerValue] = {}
    for type_name, source in sources.items():
        text = Path(source).read_text(encoding="utf-8") if isinstance(source, Path) else source
        for member, beta in _declared_in(text):
            declared[(type_name, member)] = beta
    return declared


def read_declared_versions(sources: Mapping[str, Union[str, Path]]) -> Dict[str, frozenset]:
    """Read the ``@version(...)`` each class declares, keyed by the CSDL type its file holds.

    The same rule as :func:`read_declared_markers`: the caller knows which type a file
    holds, so only the decorators are read -- and nothing is imported.
    """
    declared: Dict[str, frozenset] = {}
    for type_name, source in sources.items():
        text = Path(source).read_text(encoding="utf-8") if isinstance(source, Path) else source
        for name, versions in _versions_in(text):
            # A file holds the type its caller names; a file holding several classes says
            # which one states the gate on the class itself.
            declared[name or type_name] = versions
    return declared


def write_report(plan: MarkerPlan, edits: Optional[MarkerEdits], path: str) -> None:
    """Write the plan -- and, when a model was read, its edit list -- as JSON."""
    payload = plan.to_dict()
    if edits is not None:
        payload["edits"] = edits.to_dict()
    with open(path, "w", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=2, sort_keys=False)
        stream.write("\n")


def _flatten(bucket: Dict[str, List[str]], kind: str, value: MarkerValue, reason: str) -> Iterable[MemberMarker]:
    for type_name, members in bucket.items():
        for member in members:
            yield MemberMarker(type_name, member, kind, value, reason)


def _declared_in(text: str) -> Iterable[Tuple[str, MarkerValue]]:
    """Yield ``(odata name, beta value)`` for every ``@odata(...)`` in the source."""
    for node in ast.walk(ast.parse(text)):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call) or not isinstance(decorator.func, ast.Name):
                continue
            if decorator.func.id != "odata":
                continue
            keywords = {keyword.arg: keyword.value for keyword in decorator.keywords if keyword.arg}
            name = _literal(keywords.get("name"))
            beta = _literal(keywords.get("beta"))
            if isinstance(name, str) and beta is not None:
                yield name, beta


def _versions_in(text: str) -> Iterable[Tuple[Optional[str], frozenset]]:
    """Yield ``(odata type name, versions)`` for every ``@version(...)`` a class declares."""
    for node in ast.walk(ast.parse(text)):
        if not isinstance(node, ast.ClassDef):
            continue
        versions = _declared_roots(node)
        if versions:
            yield _odata_name_of(node), versions


def _declared_roots(class_node: ast.ClassDef) -> frozenset:
    """The service roots ``@version("beta")`` names, as written."""
    for decorator in class_node.decorator_list:
        if not isinstance(decorator, ast.Call) or getattr(decorator.func, "id", None) != "version":
            continue
        return frozenset(
            argument.value
            for argument in decorator.args
            if isinstance(argument, ast.Constant) and isinstance(argument.value, str)
        )
    return frozenset()


def _odata_name_of(node: ast.ClassDef) -> Optional[str]:
    """The ``_odata_type_name`` a class states, if it states one."""
    for statement in node.body:
        if not isinstance(statement, ast.Assign):
            continue
        targets = [target.id for target in statement.targets if isinstance(target, ast.Name)]
        value = statement.value
        if targets == ["_odata_type_name"] and isinstance(value, ast.Constant) and isinstance(value.value, str):
            return value.value
    return None


def _literal(node: Optional[ast.expr]) -> MarkerValue:
    if isinstance(node, ast.Constant) and isinstance(node.value, (bool, str)):
        return node.value
    return None
