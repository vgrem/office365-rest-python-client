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
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Tuple, Union

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


@dataclass
class MarkerPlan:
    """Every marker the target snapshot justifies, across the whole model."""

    base: str
    target: str
    markers: List[MemberMarker]

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
        )

    def to_dict(self) -> dict:
        return {
            "metadata": {"base": self.base, "target": self.target},
            "count": len(self.markers),
            "markers": [marker.to_dict() for marker in self.markers],
        }

    def render(self) -> str:
        counts = {reason: len(self.by_reason(reason)) for reason in (BETA_ONLY, RENAMED, STABLE_ONLY)}
        return (
            f"{self.target} markers: {len(self.markers)} total -- "
            f"{counts[BETA_ONLY]} beta-only, {counts[RENAMED]} renamed, {counts[STABLE_ONLY]} stable-only"
        )


@dataclass
class MarkerEdits:
    """What a model has to do to carry exactly the markers its snapshots justify."""

    added: List[MemberMarker]
    changed: List[MemberMarker]
    removed: List[MemberMarker]

    @property
    def is_empty(self) -> bool:
        return not (self.added or self.changed or self.removed)

    @property
    def count(self) -> int:
        return len(self.added) + len(self.changed) + len(self.removed)

    def to_dict(self) -> dict:
        return {
            "count": self.count,
            "added": [marker.to_dict() for marker in self.added],
            "changed": [marker.to_dict() for marker in self.changed],
            "removed": [marker.to_dict() for marker in self.removed],
        }

    def render(self) -> str:
        if self.is_empty:
            return "beta markers: up to date"
        return f"beta markers: {len(self.added)} to add, {len(self.changed)} to change, {len(self.removed)} to remove"


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
    return MarkerPlan(base=delta.base, target=delta.target, markers=markers)


def compare_markers(plan: MarkerPlan, declared: Mapping[Tuple[str, str], MarkerValue]) -> MarkerEdits:
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


def _literal(node: Optional[ast.expr]) -> MarkerValue:
    if isinstance(node, ast.Constant) and isinstance(node.value, (bool, str)):
        return node.value
    return None
