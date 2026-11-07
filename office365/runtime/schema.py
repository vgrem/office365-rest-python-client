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
    Event._schema.content_columns  # what a request may send
    Event._schema.by_attr  # python attribute -> OData name
    Event._schema.declared_limits()  # the @limit declarations of the type and its members

A declaration rides one of two carriers: a getter in the class body, which is what a
``ClientObject`` states, or a dataclass field's metadata, which is what a ``ClientValue``
states because a plain field has nowhere else to say it. Both are read by the same
builder, so which carrier a type chose is invisible to anyone asking the schema.

Both carriers are named by the finished class: a getter by the class body that states it,
a field by the ``dataclass`` pass that gives it the name it is read as. So the schema is
read once the class is complete -- in ``__init_subclass__``, after ``dataclass`` has run,
for a value and for an object alike -- and :meth:`TypeSchema.of` is an attribute read.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass, replace
from functools import cached_property
from types import MappingProxyType
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Tuple

from office365.runtime.limits import Limit, LimitDecl, collect_class_limits, collect_limit_meta
from office365.runtime.types.odata_property import (
    _ODATA_MARKER,
    IDENTITIES,
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


def _inherited_properties(model: type) -> Mapping[str, ODataPropertyMeta]:
    """The declarations ``model`` inherits from the nearest base that declares any."""
    for base in model.__mro__[1:]:
        inherited = TypeSchema.of(base)
        if inherited.properties:
            return inherited.properties
    return _EMPTY_MAP


def _collect_properties(model: type) -> Dict[str, ODataPropertyMeta]:
    """The ``@odata`` declarations of ``model``, its base class's first.

    Returns a fresh dict: a subclass inherits its base class's declarations but must
    never be able to add one to them.
    """
    properties: Dict[str, ODataPropertyMeta] = dict(_inherited_properties(model))
    for attr_name, declared in _declarations(model):
        # The carrier is the only place that knows which attribute reads it.
        declared.attr = attr_name
        properties[declared.name] = declared
    return properties


def _declarations(model: type) -> Iterator[Tuple[str, ODataPropertyMeta]]:
    """Every declaration ``model`` states, with the attribute that reads it.

    A field states its declaration in ``field(metadata=odata(...))``, and the decorator
    that declared the class gave it a name, so fields are taken the way every other
    dataclass consumer takes them. A getter states it on the function, and the class body
    names it, which is the one case where the body is the carrier of the name too.
    """
    if is_dataclass(model):
        for declared in fields(model):
            metadata = declared.metadata.get(_ODATA_MARKER)
            if metadata is not None:
                yield declared.name, metadata
    for attr_name, attr in model.__dict__.items():
        metadata = getattr(getattr(attr, "fget", attr), _ODATA_MARKER, None)
        if metadata is not None:
            yield attr_name, metadata


def _class_facts(model: type) -> Dict[str, Any]:
    """What a class states about itself rather than about one of its members."""
    return {
        "class_limits": collect_class_limits(model),
        "member_limits": MappingProxyType(collect_limit_meta(model)),
        "key": tuple(getattr(model, "_key", ())),
        "versions": frozenset(getattr(model, "_versions", ())),
    }


@dataclass(frozen=True)
class TypeSchema:
    """The declarations of one model class.

    Immutable on purpose: a class fact that a consumer can edit is a class fact that
    drifts. The ``ODataPropertyMeta`` rows inside ``properties`` are shared with the
    class body that declared them (a getter carries its own row).
    """

    #: OData name -> declaration, in declaration order (base class first). The only table
    #: a schema states: every projection below is read from it, on first ask, so a class
    #: fact cannot drift from the declarations that state it.
    properties: Mapping[str, ODataPropertyMeta] = field(default_factory=_empty_map)
    #: The class name, for the one error a schema raises by itself.
    name: str = ""
    #: The ``@limit`` declarations on the type itself, accumulated up the hierarchy: a
    #: subclass is subject to its base class's limits and its own.
    class_limits: Tuple[LimitDecl, ...] = ()
    #: Member name -> the ``@limit`` declarations carried by that method or property.
    member_limits: Mapping[str, Tuple[LimitDecl, ...]] = field(default_factory=_empty_map)
    #: The property that spells the type's identity, from ``@key(...)`` on the class --
    #: inherited, so a derived type is addressed the way its base is. Empty means the
    #: family's reader answers its own default (``id``, ``Id``).
    key: Tuple[str, ...] = ()
    #: The service roots whose metadata declares the type, from ``@version(...)`` on the
    #: class. Empty means every root: a type that states nothing is served everywhere it
    #: is reachable from.
    versions: frozenset[str] = frozenset()

    @staticmethod
    def of(model: Any) -> TypeSchema:
        """The schema of ``model``, which its class built when it was created.

        ``model`` is a class or an instance of one: the question is about the type, and a
        getter asking which name it declares is asking for its own type's schema.

        Read from the class itself, never inherited: ``vars()`` is what is read, so a
        subclass that declares nothing answers its own empty schema rather than its
        base's. A class that states no declarations at all answers the empty schema.
        """
        return vars(model if isinstance(model, type) else type(model)).get("_schema", EMPTY)

    @classmethod
    def build(cls, model: type) -> TypeSchema:
        """Read the declarations of ``model``, inheriting its base class's.

        Only what the class states is read here: the properties, the ``@limit`` rows and
        the two class-level decorators. Every projection below is derived from
        :attr:`properties` on first ask, so a class that declares two members is built as
        cheaply as one that declares two hundred.
        """
        return cls(
            properties=MappingProxyType(_collect_properties(model)),
            name=model.__name__,
            **_class_facts(model),
        )

    @classmethod
    def rebuild(cls, model: type) -> None:
        """Restate the class-level facts a decorator has just written.

        The declarations are read once, when the class is declared, so a ``@limit``, a
        ``@key`` or a ``@version`` written above that declaration is read by nothing until
        it asks for this. Only those facts are restated, because they are the only ones a
        decorator states: the properties cannot have changed, and restating them is what a
        value could not do anyway, ``__init_subclass__`` having already read its fields.
        """
        model._schema = replace(model._schema, **_class_facts(model))

    @cached_property
    def by_attr(self) -> Mapping[str, str]:
        """Python attribute name -> OData name, for the declarations a getter carries."""
        by_attr: Dict[str, str] = {}
        for name, declared in self.properties.items():
            if declared.attr:
                # First declaration wins, as the scan this replaces did: one getter can be
                # declared under more than one OData name.
                by_attr.setdefault(declared.attr, name)
        return MappingProxyType(by_attr)

    @cached_property
    def columns(self) -> Tuple[str, ...]:
        """The OData names ``$select`` accepts: the columns the type's own resource projects.

        A navigation property is left out -- the service reaches it through the path, not
        through a projection -- and so is a column declared ``selectable=False``, which is
        how a member says its own resource refuses to project it.
        """
        return tuple(
            name for name, declared in self.properties.items() if not declared.navigation and declared.selectable
        )

    @cached_property
    def navigations(self) -> Tuple[str, ...]:
        """The OData names that are links: what a path may walk through."""
        return tuple(name for name, declared in self.properties.items() if declared.navigation)

    @cached_property
    def expansions(self) -> Tuple[str, ...]:
        """The OData names ``$expand`` can reach, a subset of :attr:`navigations`.

        A link is not a promise: ``$expand`` on ``Event.extensions`` is refused unless a
        ``$filter`` is supplied, so a declaration may say ``expandable=False`` and keep
        the name out of here while the link itself stays a navigation.
        """
        return tuple(name for name, declared in self.properties.items() if declared.navigation and declared.expandable)

    @cached_property
    def readonly(self) -> frozenset[str]:
        """OData names the service assigns: a response carries them, a request may not."""
        return frozenset(name for name, declared in self.properties.items() if declared.readonly)

    @cached_property
    def content_columns(self) -> Tuple[str, ...]:
        """The columns a request may send: the projection minus the names the service assigns.

        A name stays here when nothing declares the service owns it, so the answer is the
        model's own statement of direction rather than a guess from the name. A navigation
        is already absent from :attr:`columns`, so a link the service also assigns
        (``Event.attachments``) is left out once -- subtracting ``readonly`` from the
        columns instead counts it as a column a request could send, which is what this
        projection replaces.

        A column the type does not declare is absent here and from :attr:`columns` alike,
        so this answers "may I send this name?" for the model's vocabulary and not "is
        this key content?" for a payload: a list's site columns exist on the wire and not
        in the CSDL, and a caller filtering a record by this set would drop them.
        """
        return tuple(name for name in self.columns if name not in self.readonly)

    @cached_property
    def persistable(self) -> frozenset[str]:
        """OData names a request always sends, even when nobody set them."""
        return frozenset(name for name, declared in self.properties.items() if declared.persist)

    @cached_property
    def system(self) -> frozenset[str]:
        """OData names the metadata does not declare: the service spells them on the payload."""
        return frozenset(name for name, declared in self.properties.items() if declared.system)

    @cached_property
    def beta_names(self) -> Mapping[str, str]:
        """OData name -> the name the preview root spells it with, where they differ."""
        return MappingProxyType(
            {name: declared.beta for name, declared in self.properties.items() if isinstance(declared.beta, str)}
        )

    @cached_property
    def canonical_names(self) -> Mapping[str, str]:
        """The reverse of :attr:`beta_names`: a preview name -> the name the model holds."""
        return MappingProxyType({preview: name for name, preview in self.beta_names.items()})

    @cached_property
    def beta_only(self) -> frozenset[str]:
        """Names only the preview root declares: a stable client cannot name them."""
        return frozenset(name for name, declared in self.properties.items() if declared.beta is True)

    @cached_property
    def stable_only(self) -> frozenset[str]:
        """Names only the stable root declares: a preview client cannot name them either."""
        return frozenset(name for name, declared in self.properties.items() if declared.beta is False)

    @cached_property
    def facets(self) -> Mapping[str, Tuple[str, ...]]:
        """Facet name -> the declared columns that play it, in declaration order.

        A facet is a role a caller asks for without spelling the names (an item's
        authorship, its own access control, its approval state), and it is taken from
        :attr:`columns`, so a faceted name the type declares unselectable is not offered
        through it either.
        """
        return MappingProxyType(
            {
                facet: tuple(name for name in self.columns if self.properties[name].facet == facet)
                for facet in sorted({declared.facet for declared in self.properties.values() if declared.facet})
            }
        )

    @cached_property
    def identities(self) -> Tuple[str, ...]:
        """The OData names that say what the object is, strongest first.

        Taken from :attr:`columns`, so a name the type's own resource refuses to project
        is not offered as an identification either. Ordered by the role rather than by the
        class body: a caller that has to name an object it did not create can use the
        first spelling wherever it is, the second only inside the site collection.
        """
        rank = {identity: index for index, identity in enumerate(IDENTITIES)}
        named = (name for name in self.columns if self.properties[name].identity in rank)
        return tuple(sorted(named, key=lambda name: rank[str(self.properties[name].identity)]))

    def declared(self, attr: str) -> Optional[ODataPropertyMeta]:
        """The declaration the Python attribute ``attr`` carries, if any."""
        name = self.by_attr.get(attr)
        return self.properties.get(name) if name is not None else None

    def name_of(self, attr: str) -> str:
        """The OData name the Python attribute ``attr`` declares.

        Raises:
            AttributeError: when the attribute carries no declaration, naming the
                declared attributes so a typo fails here rather than as ``None``
                further down the read path.
        """
        name = self.by_attr.get(attr)
        if name is not None:
            return name
        declared = ", ".join(sorted(self.by_attr))
        raise AttributeError(f"{self.name}.{attr} is not a declared property; declared: {declared}")

    def columns_of_facet(self, facet: str) -> Tuple[str, ...]:
        """The declared columns that play ``facet``: the names a ``$select`` may carry."""
        return self.facets.get(facet, ())

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

        A projection is bulk by nature -- :attr:`columns` is a class-level list of
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
