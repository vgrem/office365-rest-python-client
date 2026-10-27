"""Compare two OData metadata snapshots without touching the model.

The question this answers is "what changed between these two service roots", and it
answers it in the three shapes a change has: a member was **added** to the target, a
member was **lost** by it, or a member is **the same member under another name**. The
third one is not a detail -- Graph's beta renames in place, so ``accessPackage.catalog``
becomes ``accessPackageCatalog``, ``state`` becomes ``assignmentState``, and 41 types
are affected -- and reporting it as "one added + one removed" would make an
unambiguous change look like two independent ones. Every downstream consumer needs the
distinction: the marker pass writes ``beta="accessPackageCatalog"`` for a rename and
``beta=True`` for an addition, and only a rename may rewrite a wire name in place.

Pairing is deliberately conservative. A rename is claimed only when the names relate
(the normalized base name is the tail of the target name, or the target shortened it)
**and** the pairing is unambiguous in both directions: if two lost members could both
be the origin of one gained name, nothing is claimed and the members stay in the
added/lost buckets, with the ambiguity listed so a human can settle it.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from generator.odata.model import ODataModel

#: How many names to show per bucket in the text report; the JSON has them all.
_PREVIEW = 8

#: Shorter name fragments match too much to be worth calling a rename: ``name`` is
#: the tail of ``displayName`` and of half the model, ``state`` is not.
_MIN_RENAME_TAIL = 5

#: A target that *shortened* the name (``completedDateTime`` -> ``completedDate``)
#: has to keep this much of it, or "a cell of the same table" would count as a rename.
_MIN_RENAME_STEM = 6

#: The two member kinds the model turns into attributes. Kept apart so a property is
#: never paired with a navigation that happens to be named after it.
PROPERTY = "property"
NAVIGATION = "navigation"
METHOD = "method"


@dataclass(frozen=True)
class MemberTypeConflict:
    """One member the two snapshots declare with different EDM types."""

    type_name: str
    member: str
    base_type: str
    target_type: str


@dataclass(frozen=True)
class EnumValueChange:
    """One enum member whose numeric value differs between the snapshots."""

    type_name: str
    member: str
    base_value: str
    target_value: str


@dataclass(frozen=True)
class MemberRename:
    """The same member, under a different name in the target snapshot."""

    type_name: str
    kind: str
    base: str
    target: str


@dataclass(frozen=True)
class RenameCandidate:
    """A lost member that resembles gained ones, without an unambiguous pairing."""

    type_name: str
    kind: str
    base: str
    targets: Tuple[str, ...]


@dataclass
class MetadataDelta:
    """Differences between a base snapshot and a target snapshot.

    Every member that exists in both snapshots appears in exactly one place: the
    ``renamed`` list when the name changed, the ``*_only_in_*`` buckets when only one
    snapshot declares it, and nowhere at all when the two agree.
    """

    base: str
    target: str
    types_only_in_target: List[str] = field(default_factory=list)
    types_only_in_base: List[str] = field(default_factory=list)
    properties_only_in_target: Dict[str, List[str]] = field(default_factory=dict)
    properties_only_in_base: Dict[str, List[str]] = field(default_factory=dict)
    navigations_only_in_target: Dict[str, List[str]] = field(default_factory=dict)
    navigations_only_in_base: Dict[str, List[str]] = field(default_factory=dict)
    enum_members_only_in_target: Dict[str, List[str]] = field(default_factory=dict)
    enum_members_only_in_base: Dict[str, List[str]] = field(default_factory=dict)
    methods_only_in_target: Dict[str, List[str]] = field(default_factory=dict)
    methods_only_in_base: Dict[str, List[str]] = field(default_factory=dict)
    member_type_conflicts: List[MemberTypeConflict] = field(default_factory=list)
    enum_value_changes: List[EnumValueChange] = field(default_factory=list)
    renamed: List[MemberRename] = field(default_factory=list)
    rename_candidates: List[RenameCandidate] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        """True when the target snapshot declares nothing the base does not."""
        return not any(
            (
                self.types_only_in_target,
                self.types_only_in_base,
                self.properties_only_in_target,
                self.properties_only_in_base,
                self.navigations_only_in_target,
                self.navigations_only_in_base,
                self.enum_members_only_in_target,
                self.enum_members_only_in_base,
                self.methods_only_in_target,
                self.methods_only_in_base,
                self.member_type_conflicts,
                self.enum_value_changes,
                self.renamed,
            )
        )

    def to_dict(self) -> dict:
        """A JSON-serialisable view; every bucket in full, not just the preview."""
        return {
            "metadata": {"base": self.base, "target": self.target},
            "types_only_in_target": self.types_only_in_target,
            "types_only_in_base": self.types_only_in_base,
            "properties_only_in_target": self.properties_only_in_target,
            "properties_only_in_base": self.properties_only_in_base,
            "navigations_only_in_target": self.navigations_only_in_target,
            "navigations_only_in_base": self.navigations_only_in_base,
            "enum_members_only_in_target": self.enum_members_only_in_target,
            "enum_members_only_in_base": self.enum_members_only_in_base,
            "methods_only_in_target": self.methods_only_in_target,
            "methods_only_in_base": self.methods_only_in_base,
            "member_type_conflicts": [conflict.__dict__ for conflict in self.member_type_conflicts],
            "enum_value_changes": [change.__dict__ for change in self.enum_value_changes],
            "renamed": [rename.__dict__ for rename in self.renamed],
            "rename_candidates": [
                {**candidate.__dict__, "targets": list(candidate.targets)} for candidate in self.rename_candidates
            ],
        }

    def render(self) -> str:
        """A short human summary; the JSON report carries the whole answer."""
        if self.is_empty:
            return f"{self.target} declares nothing {self.base} does not."
        lines = [f"{self.base} -> {self.target}"]
        lines.append(
            f"  types         : {len(self.types_only_in_target)} only in target, "
            f"{len(self.types_only_in_base)} only in base"
        )
        for label, bucket in (
            ("properties", self.properties_only_in_target),
            ("navigations", self.navigations_only_in_target),
            ("enum members", self.enum_members_only_in_target),
            ("methods", self.methods_only_in_target),
        ):
            lines.append(f"  {label:<14}: {_spread(bucket)}")
        for label, bucket in (
            ("properties lost", self.properties_only_in_base),
            ("navigations lost", self.navigations_only_in_base),
            ("enum members lost", self.enum_members_only_in_base),
            ("methods lost", self.methods_only_in_base),
        ):
            lines.append(f"  {label:<14}: {_spread(bucket)}")
        lines.append(f"  type conflicts: {len(self.member_type_conflicts)} same name, different EDM type")
        lines.append(f"  enum values   : {len(self.enum_value_changes)} whose numeric value differs")
        lines.append(f"  renames       : {_rename_spread(self.renamed)}")
        if self.rename_candidates:
            lines.append(f"  rename doubts : {len(self.rename_candidates)} left unpaired (see --diff-report)")
        for heading, names in (
            ("types only in target", self.types_only_in_target),
            ("types only in base", self.types_only_in_base),
        ):
            if names:
                lines.append(f"\n{heading} (first {_PREVIEW} of {len(names)}):")
                lines.extend(f"  {name}" for name in names[:_PREVIEW])
        if self.member_type_conflicts:
            lines.append(f"\nsame name, different EDM type (first {_PREVIEW}):")
            lines.extend(
                f"  {conflict.type_name.split('.')[-1]}.{conflict.member}: "
                f"{conflict.base_type} -> {conflict.target_type}"
                for conflict in self.member_type_conflicts[:_PREVIEW]
            )
        if self.renamed:
            lines.append(f"\nrenamed in the target (first {_PREVIEW}):")
            lines.extend(
                f"  {rename.kind} {_short(rename.type_name)}.{rename.base} -> {rename.target}"
                for rename in self.renamed[:_PREVIEW]
            )
        return "\n".join(lines)


def diff_metadata(base: ODataModel, target: ODataModel, base_label: str, target_label: str) -> MetadataDelta:
    """Compute what ``target`` declares that ``base`` does not, and vice versa."""
    delta = MetadataDelta(base=base_label, target=target_label)
    base_names, target_names = set(base.types), set(target.types)
    delta.types_only_in_target = sorted(target_names - base_names)
    delta.types_only_in_base = sorted(base_names - target_names)

    for name in sorted(base_names & target_names):
        _diff_type(base.types[name], target.types[name], delta)
    return delta


def _diff_type(base_type, target_type, delta: MetadataDelta) -> None:
    type_name = target_type.FullName
    base_members = _members_by_kind(base_type)
    target_members = _members_by_kind(target_type)

    for kind, bucket_in_target, bucket_in_base in (
        (PROPERTY, delta.properties_only_in_target, delta.properties_only_in_base),
        (NAVIGATION, delta.navigations_only_in_target, delta.navigations_only_in_base),
    ):
        lost = sorted(set(base_members[kind]) - set(target_members[kind]))
        gained = sorted(set(target_members[kind]) - set(base_members[kind]))
        renames = _pair_renames(lost, gained)
        delta.renamed.extend(MemberRename(type_name, kind, before, after) for before, after in sorted(renames.items()))
        if remaining := [name for name in lost if name not in renames]:
            bucket_in_base[type_name] = remaining
        if remaining := _leftover(gained, renames):
            bucket_in_target[type_name] = remaining
        delta.rename_candidates.extend(_ambiguities(type_name, kind, lost, gained, renames))

    for member in sorted(set(base_type.Properties) & set(target_type.Properties)):
        before, after = base_type.Properties[member].TypeName, target_type.Properties[member].TypeName
        if before != after:
            delta.member_type_conflicts.append(MemberTypeConflict(type_name, member, before or "", after or ""))

    _diff_enum(base_type, target_type, delta)

    added_methods = sorted(set(target_type.Methods) - set(base_type.Methods))
    if added_methods:
        delta.methods_only_in_target[type_name] = added_methods
    removed_methods = sorted(set(base_type.Methods) - set(target_type.Methods))
    if removed_methods:
        delta.methods_only_in_base[type_name] = removed_methods


def _members_by_kind(schema) -> Dict[str, List[str]]:
    """Split a type's members the way the model splits them: property vs navigation."""
    members: Dict[str, List[str]] = {PROPERTY: [], NAVIGATION: []}
    for name, prop in schema.Properties.items():
        members[NAVIGATION if prop.IsNavigation else PROPERTY].append(name)
    return members


def _diff_enum(base_type, target_type, delta: MetadataDelta) -> None:
    base_members, target_members = base_type.Members, target_type.Members
    if added := sorted(set(target_members) - set(base_members)):
        delta.enum_members_only_in_target[target_type.FullName] = added
    if removed := sorted(set(base_members) - set(target_members)):
        delta.enum_members_only_in_base[target_type.FullName] = removed
    for member in sorted(set(base_members) & set(target_members)):
        before, after = base_members[member].Value, target_members[member].Value
        if before != after:
            delta.enum_value_changes.append(EnumValueChange(target_type.FullName, member, before or "", after or ""))


def _leftover(gained: Sequence[str], renames: Mapping[str, str]) -> List[str]:
    """The gained names that no rename claimed."""
    claimed = set(renames.values())
    return [name for name in gained if name not in claimed]


def _rename_score(before: str, after: str) -> int:
    """How strongly ``after`` looks like ``before`` renamed, 0 when it does not.

    Beta grows names by prefixing the family they belong to
    (``catalog`` -> ``accessPackageCatalog``) and shrinks them by dropping a word
    (``completedDateTime`` -> ``completedDate``); both keep a recognizable stem, which
    is what is scored -- the longer the stem, the stronger the claim.
    """
    lost, gained = _normalize(before), _normalize(after)
    if len(lost) < _MIN_RENAME_TAIL:
        return 0
    if gained.endswith(lost):
        return len(lost)
    if len(gained) >= _MIN_RENAME_STEM and lost.startswith(gained):
        return len(gained)
    return 0


def _pair_renames(lost: Sequence[str], gained: Sequence[str]) -> Dict[str, str]:
    """Pair lost and gained members, claiming only unambiguous ones.

    Both sides have to agree: ``before`` has no closer candidate than ``after`` and
    ``after`` has no closer candidate than ``before``. Anything less stays unpaired,
    because a wrong pair would rewrite a wire name that the service never renamed.
    """
    scores = {(before, after): score for before in lost for after in gained if (score := _rename_score(before, after))}
    pairs: Dict[str, str] = {}
    while True:
        free_lost = [name for name in lost if name not in pairs]
        claimed = set(pairs.values())
        free_gained = [name for name in gained if name not in claimed]
        progressed = False
        for before in free_lost:
            forward = {after: scores[(before, after)] for after in free_gained if (before, after) in scores}
            if not forward:
                continue
            best_after = max(forward.values())
            closest = [after for after, score in forward.items() if score == best_after]
            if len(closest) != 1:
                continue
            after = closest[0]
            backward = {name: scores[(name, after)] for name in free_lost if (name, after) in scores}
            best_before = max(backward.values())
            holders = [name for name, score in backward.items() if score == best_before]
            if holders == [before]:
                pairs[before] = after
                progressed = True
        if not progressed:
            return pairs


def _ambiguities(
    type_name: str,
    kind: str,
    lost: Sequence[str],
    gained: Sequence[str],
    renames: Mapping[str, str],
) -> List[RenameCandidate]:
    """Lost members that resemble a gained one but were not paired: a human decides."""
    claimed = set(renames.values())
    candidates: List[RenameCandidate] = []
    for before in lost:
        if before in renames:
            continue
        similar = sorted(after for after in gained if after not in claimed and _rename_score(before, after))
        if similar:
            candidates.append(RenameCandidate(type_name, kind, before, tuple(similar)))
    return candidates


def _normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _short(full_name: str) -> str:
    return full_name.rsplit(".", maxsplit=1)[-1]


def _rename_spread(renames: Iterable[MemberRename]) -> str:
    """``86 members in 41 types (e.g. AccessPackage: catalog -> accessPackageCatalog)``."""
    renames = list(renames)
    if not renames:
        return "0"
    types = {rename.type_name for rename in renames}
    sample = renames[0]
    return (
        f"{len(renames)} members in {len(types)} types "
        f"(e.g. {_short(sample.type_name)}.{sample.base} -> {sample.target})"
    )


def _spread(bucket: Dict[str, List[str]], preview: int = 4) -> str:
    """``438 types / 2084 names`` plus a couple of examples."""
    if not bucket:
        return "0"
    total = sum(len(names) for names in bucket.values())
    sample = next(iter(bucket.items()))
    shown = ", ".join(sample[1][:preview])
    return f"{len(bucket)} types / {total} names (e.g. {_short(sample[0])}: {shown})"


def write_report(delta: MetadataDelta, path: str) -> None:
    """Write the full delta as JSON."""
    with open(path, "w", encoding="utf-8") as stream:
        json.dump(delta.to_dict(), stream, indent=2, sort_keys=False)
        stream.write("\n")
