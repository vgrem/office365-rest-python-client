from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Callable, Dict, Optional, TypeVar, Union

_ODATA_MARKER = "__odata__"
_T = TypeVar("_T")

PREVIEW = "beta"
"""The version token of the preview service root -- ``GraphVersion.BETA.value``.

The token is spelled here because it is what a declaration compares a client's
version against, and a declaration is written by the generator, not by hand:
``beta=PREVIEW`` -- written as ``beta=True`` -- is the difference between a member
both service roots declare and one only the preview one does, and ``@version(PREVIEW)``
-- written as ``@version("beta")`` -- is the same difference for a whole type.
"""

_FIELD_DECLARATIONS: Dict[type, Dict[str, "ODataPropertyMeta"]] = {}


def request_version(context: Any) -> Optional[str]:
    """The API version a client addresses, when the client names one at all.

    A SharePoint context addresses no version of anything, so the answer is ``None``
    and no declaration that states a version applies to it. The runtime asks the
    context instead of importing a service enum: Graph states the fact on
    ``GraphRequest.version``, and that is all the runtime needs to know.
    """
    version = getattr(context, "version", None)
    return getattr(version, "value", version)


class NotSupportedInVersion(ValueError):
    """A member the model holds, but the client's API version does not declare.

    There is one model tree for both service roots, so a preview member is an
    attribute of the class a stable client instantiates. Holding it is not the error
    -- naming it is: a stable client that selects it, or sends it, would be describing
    an entity the stable root has no schema for.
    """

    def __init__(self, member: str, version: Optional[str], declared_by: Optional[str] = None) -> None:
        super().__init__(
            f"{member} is declared by the {declared_by} service root only, "
            f"and this client addresses {version if version is not None else 'no version'}"
            if declared_by is not None
            else f"{member} is not declared by the {version} service root"
        )
        self.member = member
        self.version = version
        self.declared_by = declared_by


@dataclass(frozen=True)
class Compare:
    """What the service treats as the same value, declared where the field is.

    A response and the payload that created it seldom agree byte for byte: the service
    fills a name in from an address, stores a birthday at a time of day nobody set,
    keeps a list of labels as a set. Each of those is a fact about one field, so it is
    stated on that field and applied by one profile
    (:data:`office365.runtime.odata.comparable.COMPARABLE`), instead of being re-derived
    by every caller that has to compare two spellings.
    """

    #: A collection the service keeps as a set: the same members are the same value.
    unordered: bool = False
    #: Text the service treats case-insensitively.
    casefold: bool = False
    #: The sibling field the service fills this one in from when it is unset.
    fallback: Optional[str] = None
    #: What an unset value means (an attendee with no ``type`` is a required one).
    default: Any = None
    #: A named reduction of the spelled value: ``"date"``, ``"wall-clock"`` or ``"text"``.
    format: Optional[str] = None
    #: Owned by someone else (the service, the attendee): not part of the sender's value.
    ignore: bool = False
    #: What identifies the value: with this field empty the value is nobody, and says nothing.
    key: bool = False

    def __post_init__(self) -> None:
        from office365.runtime.odata.comparable import FORMATS

        if self.format is not None and self.format not in FORMATS:
            raise ValueError(f"unknown comparison format {self.format!r}; known: {', '.join(sorted(FORMATS))}")


@dataclass
class ODataPropertyMeta:
    """Metadata for an ``@odata``-declared property.

    ``name`` is the JSON/OData key; ``attr`` is the Python attribute name,
    filled in by ``ClientObject.__init_subclass__`` at class creation.
    """

    name: str
    attr: str = ""
    persist: bool = False
    readonly: bool = False
    navigation: bool = False
    #: Whether ``$expand`` reaches this navigation with no further arguments. The CSDL
    #: says a member is a link; it does not say the service will follow it, so a link
    #: that needs a ``$filter`` says so here.
    expandable: bool = True
    #: The CSDL this client is generated from does not declare the name: the service
    #: spells it on the *item* payload, which the metadata never describes. A list item
    #: answers ``AuthorId``, ``EditorId``, ``Created`` and ``Modified``; a page adds
    #: ``FileLeafRef``, ``WikiField`` and ``OData__ModerationStatus``. ``SP.ListItem``'s
    #: own declaration is 24 names long and carries none of the seven.
    system: bool = False
    filterable: bool = False
    nullable: bool = True
    sortable: bool = False
    searchable: bool = False
    compare: Optional[Compare] = None
    description: str = ""
    #: What the preview service root does with this member, when it differs from the
    #: stable root. One attribute, four answers, because it is one fact::
    #:
    #:     beta=None                    every root declares it, same spelling
    #:     beta="accessPackageCatalog"  every root declares it, the preview root renames it
    #:     beta=True                    only the preview root declares it
    #:     beta=False                   only the stable root declares it
    #:
    #: Beta renames in place -- ``accessPackage.catalog`` is ``accessPackageCatalog``
    #: there -- so one member can have two wire names. The model holds one of them (the
    #: stable spelling) and translates at the two edges, which is why a generated getter
    #: reads a name that is the same under either client.
    beta: Optional[Union[bool, str]] = None


class odata(dict):
    """Declare the OData metadata of one property.

    A ``ClientObject`` has a property to decorate, so the declaration is applied to
    it::

        @odata(name="start")
        def start(self): ...

    A ``ClientValue`` is a dataclass: its fields are annotations, not properties, so
    the same declaration rides along in the field's metadata instead::

        start: DateTimeTimeZone | None = field(default=None, metadata=odata(name="start"))

    One name, one ``ODataPropertyMeta``, two carriers, because a field and a property
    are both a name plus an annotation. Being a ``Mapping`` is what makes the second
    form possible; being callable is what keeps the first one byte-identical.

    ``readonly=True`` marks a value the service assigns -- its id, its audit stamps,
    the organizer it resolved, the response it recorded: a response carries it, a
    request must not. (``Org.OData.Core.V1`` spells the same fact ``Computed`` or
    ``Immutable``; a CSOM type declares neither, so here it is curated.)
    ``navigation=True`` marks a CSDL ``NavigationProperty``, after the element that
    declares it: it is reached with ``$expand`` and cannot appear in ``$select``.
    ``expandable=False`` narrows that to the links ``$expand`` will not follow on its own
    -- the CSDL knows the member is a link, only the service knows it demands an argument.
    ``system=True`` records where the name comes from: the metadata does not declare it,
    the service does. Everything a list item carries beyond ``Id`` is such a name, so a
    reader who sees one knows the CSDL is silent about it and the wire is not -- and
    ``tests/unit/test_odata_metadata.py`` keeps the flag equal to that fact.
    ``beta=`` records what the preview root does with the member -- declares it the same,
    declares it under another name, declares it alone, or dropped it -- because one model
    tree serves both roots and that is the whole difference (see also :func:`key`, which
    states the same kind of fact about a type rather than about one of its attributes)::

        @odata(name="catalog", beta="accessPackageCatalog")  # both roots, renamed in preview
        def catalog(self): ...


        @odata(name="uniqueName", beta=True)  # the preview root only
        def unique_name(self): ...
    """

    meta: ODataPropertyMeta

    def __init__(self, name: str, **attrs: bool | str | None | Compare) -> None:
        self.meta = ODataPropertyMeta(name=name, **attrs)  # type: ignore[arg-type]
        super().__init__({_ODATA_MARKER: self.meta})

    def __call__(self, method: _T) -> _T:
        target = method.fget if isinstance(method, property) else method  # type: ignore[attr-defined]
        setattr(target, _ODATA_MARKER, self.meta)
        return method


_Cls = TypeVar("_Cls", bound=type)


def version(service_root: str, *others: str) -> Callable[[_Cls], _Cls]:
    """Declare the service roots whose metadata declares a *type*.

    One model tree serves both roots, so a class only the preview root declares is
    still an attribute of the module a stable client imports. The gate states that,
    and :func:`require_declared_version` refuses to build the object -- or a collection
    of it -- on a client addressing another root::

        @version("beta")
        class Mention(Entity): ...

    A member states the same kind of fact with ``beta=`` on ``@odata``; a type states
    it with a set of roots, which is why it is a second decorator rather than another
    argument of the first. ``@odata`` describes one attribute of an instance -- it needs
    a wire name, and on a class there is none -- while ``@version`` describes the class,
    and one decorator taking both grammars would have to branch on what it was handed.
    """
    declared = frozenset((service_root, *others))

    def decorate(cls: _Cls) -> _Cls:
        cls._versions = declared
        return cls

    return decorate


class CompositeKeyNotSupported(ValueError):
    """A type keyed by more than one property, which one path segment cannot hold.

    The CSDL allows a key to be spelled with several ``PropertyRef``s, and the preview
    snapshot declares one. The runtime addresses an entity with a single segment --
    ``<collection>/<value>`` -- so a composite key has no spelling here: stating it
    would be a claim the addressing code cannot honour.
    """


def key(*names: str) -> Callable[[_Cls], _Cls]:
    """Declare which property spells a *type's* identity.

    ``property_ref_name`` answers the question: it is what re-anchors an entity's path
    when the value is set, and what widens the ``$select`` of a read. This decorator is
    where the answer comes from, when the metadata declares one and the family default
    is wrong::

        @key("tenantId")
        class CrossTenantAccessPolicyConfigurationPartner(Entity): ...

    No declaration means the family default -- ``id`` for Graph, ``Id`` for SharePoint --
    which is what a derived type inherits, and why the snapshot leaves ``<Key>`` off most
    types. A class that writes ``property_ref_name`` itself is not decorated: the override
    is the same fact stated in place, and two spellings of one fact is the thing this
    decorator exists to remove.
    """

    def decorate(cls: _Cls) -> _Cls:
        if len(names) != 1:
            raise CompositeKeyNotSupported(
                f"{cls.__name__} is keyed by {'/'.join(names) or 'nothing'}; "
                "an entity is addressed by exactly one property"
            )
        cls._key = names
        return cls

    return decorate


def field_declarations(cls: type) -> Dict[str, ODataPropertyMeta]:
    """The declared fields of a dataclass, by attribute name.

    Empty for anything that declares nothing -- a plain dataclass, a hand-written
    value, a ``ClientObject``. Declaring is opt-in, so the 2,887 nested types keep
    their attribute names until one of them has a fact to state.
    """
    cached = _FIELD_DECLARATIONS.get(cls)
    if cached is None:
        cached = (
            {f.name: f.metadata[_ODATA_MARKER] for f in fields(cls) if _ODATA_MARKER in f.metadata}
            if is_dataclass(cls)
            else {}
        )
        _FIELD_DECLARATIONS[cls] = cached
    return cached
