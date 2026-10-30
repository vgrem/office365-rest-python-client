"""What one model type declares, as a single immutable fact.

Every question the runtime asks about a type — which columns ``$select`` may name,
which navigations ``$expand`` may reach, which names the service assigns, which
Python attribute spells which OData name — is a projection of the same declarations.
Asked separately they became six class attributes and four loops over one dict;
asked as one object they are attributes of a fact built once, when the class is
created::

    Event._schema.columns  # the columns $select accepts
    Event._schema.navigations  # what $expand can reach
    Event._schema.readonly  # what a request may not send
    Event._schema.by_attr  # python attribute -> OData name
    Event._schema.declared_limits()  # the @limit declarations of the type and its members

The build is eager because a class body is complete by the time
``ClientObject.__init_subclass__`` runs. The other half of the model cannot be: a
``ClientValue`` declares its metadata in ``field(metadata=...)``, which only exists
after ``@dataclass`` has been applied, so
:func:`office365.runtime.types.odata_property.field_declarations` stays lazy. One
:class:`~office365.runtime.types.odata_property.ODataPropertyMeta`, two moments at
which it becomes readable — and the reason the two halves do not share a builder.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Dict, Iterable, List, Mapping, Optional, Tuple

from office365.runtime.limits import Limit, LimitDecl, collect_class_limits, collect_limit_meta
from office365.runtime.types.odata_property import (
    _ODATA_MARKER,
    PREVIEW,
    NotSupportedInVersion,
    ODataPropertyMeta,
)

_EMPTY_MAP: Mapping = MappingProxyType({})


def _empty_map() -> Mapping:
    """The shared empty mapping, as a dataclass default.

    Python 3.11 refuses an unhashable *instance* as a dataclass default (3.12 relaxed
    the check back to ``list``/``dict``/``set``), and a ``mappingproxy`` is unhashable,
    so writing ``= _EMPTY_MAP`` in a class body made this module unimportable there —
    which made every model unimportable. The factory keeps the one shared instance
    without putting it in the class body.
    """
    return _EMPTY_MAP


def _collect_properties(model: type) -> Dict[str, ODataPropertyMeta]:
    """The ``@odata`` declarations of ``model``, its base class's first.

    Returns a fresh dict: a subclass inherits its base class's declarations but must
    never be able to add one to them.
    """
    inherited = getattr(model, "_schema", None)
    properties: Dict[str, ODataPropertyMeta] = dict(inherited.properties) if inherited is not None else {}
    for attr_name, attr in model.__dict__.items():
        target = attr.fget if isinstance(attr, property) else attr
        declared: Optional[ODataPropertyMeta] = getattr(target, _ODATA_MARKER, None)
        if declared is not None:
            # The getter is the carrier of the declaration, so it is also the only
            # place that knows which attribute reads it.
            declared.attr = attr_name
            properties[declared.name] = declared
    return properties


@dataclass(frozen=True)
class TypeSchema:
    """The declarations of one model class.

    Immutable on purpose: a class fact that a consumer can edit is a class fact that
    drifts. The ``ODataPropertyMeta`` rows inside ``properties`` are shared with the
    class body that declared them (a getter carries its own row).
    """

    #: OData name -> declaration, in declaration order (base class first).
    properties: Mapping[str, ODataPropertyMeta] = field(default_factory=_empty_map)
    #: The OData names ``$select`` accepts: declarations that are not navigations.
    columns: Tuple[str, ...] = ()
    #: The OData names ``$expand`` can reach.
    navigations: Tuple[str, ...] = ()
    #: Python attribute name -> OData name, for the declared getters.
    by_attr: Mapping[str, str] = field(default_factory=_empty_map)
    #: OData names the service assigns: a response carries them, a request may not.
    readonly: frozenset[str] = frozenset()
    #: OData names a request always sends, even when nobody set them.
    persistable: frozenset[str] = frozenset()
    #: OData names the metadata does not declare: the service spells them on the item
    #: payload (``system=True`` on the declaration).
    system: frozenset[str] = frozenset()
    #: The ``@limit`` declarations on the type itself, accumulated up the hierarchy: a
    #: subclass is subject to its base class's limits and its own.
    class_limits: Tuple[LimitDecl, ...] = ()
    #: Member name -> the ``@limit`` declarations carried by that method or property.
    member_limits: Mapping[str, Tuple[LimitDecl, ...]] = field(default_factory=_empty_map)
    #: OData name -> the name the preview service root spells it with, where they differ.
    #: Beta renames in place, so one member can have two wire names; the model holds one.
    beta_names: Mapping[str, str] = field(default_factory=_empty_map)
    #: The reverse of :attr:`beta_names`: a preview name -> the name the model holds.
    canonical_names: Mapping[str, str] = field(default_factory=_empty_map)
    #: Names only the preview service root declares: a stable client cannot name them.
    beta_only: frozenset[str] = frozenset()
    #: Names only the stable root declares: a preview client cannot name them either.
    stable_only: frozenset[str] = frozenset()

    @classmethod
    def build(cls, model: type) -> TypeSchema:
        """Read the declarations of ``model``, inheriting its base class's."""
        properties = _collect_properties(model)
        member_limits = MappingProxyType(collect_limit_meta(model))
        by_attr: Dict[str, str] = {}
        for name, declared in properties.items():
            if declared.attr:
                # First declaration wins, as the scan this replaces did: one getter can
                # be declared under more than one OData name.
                by_attr.setdefault(declared.attr, name)
        return cls(
            properties=MappingProxyType(properties),
            columns=tuple(
                name
                for name, declared in properties.items()
                if not declared.navigation and name not in getattr(model, "_unselectable", ())
            ),
            navigations=tuple(name for name, declared in properties.items() if declared.navigation),
            by_attr=MappingProxyType(by_attr),
            readonly=frozenset(name for name, declared in properties.items() if declared.readonly),
            persistable=frozenset(name for name, declared in properties.items() if declared.persist),
            system=frozenset(name for name, declared in properties.items() if declared.system),
            beta_names=MappingProxyType(
                {name: declared.beta for name, declared in properties.items() if isinstance(declared.beta, str)}
            ),
            canonical_names=MappingProxyType(
                {declared.beta: name for name, declared in properties.items() if isinstance(declared.beta, str)}
            ),
            beta_only=frozenset(name for name, declared in properties.items() if declared.beta is True),
            stable_only=frozenset(name for name, declared in properties.items() if declared.beta is False),
            class_limits=collect_class_limits(model),
            member_limits=member_limits,
        )

    def canonical(self, name: str) -> str:
        """The name the model holds for ``name``, whichever root spelled it.

        A preview response arrives under the preview spelling and is translated on the
        way in, so every getter -- generated or hand-written -- reads one name.
        """
        return self.canonical_names.get(name, name)

    def wire_name(self, name: str, version: Optional[str]) -> str:
        """The name ``version`` spells ``name`` with.

        Raises :class:`~office365.runtime.types.odata_property.NotSupportedInVersion`
        when the two roots disagree about the member: a stable client that sent
        ``uniqueName`` would be describing an entity the stable schema has no member
        for, and a preview client that sent a name the preview root dropped would be
        describing nothing at all.

        A client that states no version is not gated by one. ``version`` is ``None`` for
        every context that names no API version -- SharePoint addresses one service root
        and has no switch to throw -- so the markers its document carries are provenance:
        ``SP.Field.customFormatter`` is one value, not one of two spellings.
        """
        declared = self.properties.get(name)
        if declared is None or version is None:
            return name
        preview = version == PREVIEW
        if declared.beta is True and not preview:
            raise NotSupportedInVersion(name, version, PREVIEW)
        if declared.beta is False and preview:
            raise NotSupportedInVersion(name, version)
        if preview and isinstance(declared.beta, str):
            return declared.beta
        return name

    def projection(self, names: Iterable[str], version: Optional[str]) -> List[str]:
        """The names of ``names`` that ``version`` declares, spelled as it spells them.

        A projection is bulk by nature -- ``select_all()`` is a class-level list of
        names, and a manifest carries names read from another snapshot -- so a name the
        root does not declare is *dropped* here rather than raising. Refusing stays
        where one member is written (:meth:`wire_name`, and through it ``to_json``):
        that is one name, and the caller can be told which.
        """
        if version is None:
            return list(names)
        excluded = self.stable_only if version == PREVIEW else self.beta_only
        return [self.wire_name(name, version) for name in names if name not in excluded]

    def declared_limits(self) -> Tuple[Limit, ...]:
        """Every limit the type is subject to: its own, then its members'.

        A row declared on two members (``sessions`` and ``participants_v2`` share the
        per-record ceiling) is one limit, not two, so the rows come back de-duplicated
        by identity — the tuple answers "what caps this type", not "where is it written".
        """
        rows = (
            *(decl.limit for decl in self.class_limits),
            *(decl.limit for decls in self.member_limits.values() for decl in decls),
        )
        seen: set[int] = set()
        result: list[Limit] = []
        for row in rows:
            if id(row) in seen:
                continue
            seen.add(id(row))
            result.append(row)
        return tuple(result)


#: The schema of a type that declares nothing.
EMPTY = TypeSchema()
