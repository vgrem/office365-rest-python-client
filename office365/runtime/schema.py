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
    Event._schema.serializable  # what a request serializes
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

import ast
import importlib
import inspect
import re
import types
from dataclasses import dataclass, field, fields, is_dataclass, replace
from functools import cached_property
from types import MappingProxyType
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from office365.runtime.limits import Limit, LimitDecl, collect_class_limits, collect_limit_meta
from office365.runtime.types.odata_property import (
    _ODATA_MARKER,
    IDENTITIES,
    PREVIEW,
    ODataPropertyMeta,
    require_declared_member,
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
        inherited = _inherited_properties(model)
        for declared in fields(model):
            metadata = declared.metadata.get(_ODATA_MARKER)
            if metadata is None:
                # A field with no ``odata(...)`` still declares itself: its name is the
                # column and its annotation is the column's type. A base class that
                # already declared the name keeps the direction it stated, so a
                # read-only column does not become writable because a subclass restates
                # the field.
                inherited_row = inherited.get(declared.name)
                metadata = replace(inherited_row) if inherited_row is not None else ODataPropertyMeta(name=declared.name)
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
    #: The class the schema describes, for the one projection that has to ask it: a
    #: column's type is resolved from the member that declares it, not from the row.
    model: Any = field(default=None, compare=False, repr=False)
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
            model=model,
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
    def dtypes(self) -> Mapping[str, Any]:
        """OData name -> the declared (unwrapped) type of that column, or ``None``.

        The second half of a declaration: ``properties`` says which names the type
        states, this says what one cell of each holds. A column is resolved when it is
        first asked about -- hydrating a page asks about the columns the payload carries,
        a reader about the columns it is about to read -- because resolving one can
        import a module the type needed only for a type checker: a column nobody asks
        about must cost nothing. A reader that knows a type's columns before it reads a
        row asks here instead of taking a ``dtypes=`` map from the caller.
        """
        return _Dtypes(self)

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
    def serializable(self) -> frozenset[str]:
        """OData names a request serializes: the properties, minus navigations and :attr:`readonly`.

        The mirror of :attr:`readonly`, "a response carries them, a request does not": a
        name is here unless something declares the service owns it, so the answer is the
        model's statement of direction rather than a guess from the name. A navigation is
        a link and not a body, so a link the service also assigns (``Event.attachments``)
        is left out once. :attr:`columns` answers a different question -- what ``$select``
        accepts -- so a column declared ``selectable=False`` stays here: unprojectable is
        not service-owned, and ``DeviceManagement.enableLegacyPcManagement`` is what a
        ``PATCH`` sets.

        Serialized in the direction a request goes, which is what makes the name exact
        rather than convenient: ``to_json(profile=None)`` -- a response, a hydration, a
        comparison -- serializes every stored column, readonly ones included, and the
        restriction lives in the one request branch that drops them (``if k not in
        readonly``). So the axis is what a payload carries, not what the model accepts: a
        name the service assigns is still *settable* -- a hydration and ``set_property``
        both write it -- which is why ``writable`` and ``settable`` were the wrong borrow.

        A column the type does not declare is absent here and from :attr:`columns` alike,
        so this answers "may I send this name?" for the model's vocabulary and not "is
        this field settable?" for one payload: a list's site columns exist on the wire and
        not in the CSDL, and a caller filtering a record by this set would drop them.
        """
        return frozenset(
            name for name, declared in self.properties.items() if not declared.navigation and not declared.readonly
        )

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
        require_declared_member(name, declared.beta, version)
        if version == PREVIEW and isinstance(declared.beta, str):
            return declared.beta
        return name

    def hidden(self, version: Optional[str]) -> frozenset[str]:
        """The python names ``version`` does not declare -- what the instance must not offer.

        A member is named twice: as a key the service spells (``properties``) and as the
        attribute a caller writes (``by_attr``). ``dir()`` asks the second question, so
        the answer is spelled the second way, and only the members whose declaration
        states a version are candidates -- one model tree serves both roots, and a member
        both roots declare is not hidden from either.
        """
        if version is None:
            return frozenset()
        excluded = self.stable_only if version == PREVIEW else self.beta_only
        if not excluded:
            return frozenset()
        return frozenset(attr for attr, name in self.by_attr.items() if name in excluded)

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


# ── A column's type ──────────────────────────────────────────────
#
# A declaration says what a column *is*; its type is the annotation of the member that
# declares it. Generated annotations are strings in modules that import a cyclic type
# inside the getter, or only under ``TYPE_CHECKING``, so the annotation is evaluated the
# way its own module spells it -- never by asking the class as a whole, where one such
# name would leave every other column of the type untyped.

_NoneType = type(None)


def to_snake_case(name: str) -> str:
    """Convert a camelCase property name to its snake_case Python attribute."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _unwrap_type(target: Any) -> Any:
    """Strip Optional/Union wrappers from a type annotation."""
    origin = get_origin(target)
    if origin in (Union, getattr(types, "UnionType", None)):
        args = [a for a in get_args(target) if a is not _NoneType]
        return args[0] if len(args) == 1 else target
    return target


#: Module name -> the names it imports for itself, including its ``TYPE_CHECKING`` block.
_module_names: Dict[str, Dict[str, Any]] = {}


class _Dtypes(Mapping[str, Any]):
    """A type's column types, each resolved the first time it is asked about.

    A mapping, not a stored dict, because resolving a column can import a module the
    type named only for a type checker: hydrating a page must pay for the columns the
    payload carries, and a reader for the columns it reads, never for the rest. Asking
    twice resolves once; asking for an attribute spelling answers the property it spells.
    """

    def __init__(self, schema: TypeSchema) -> None:
        self._schema = schema
        self._resolved: Dict[str, Any] = {}

    def __getitem__(self, name: str) -> Any:
        if name not in self._resolved:
            self._resolved[name] = _resolve_declared_type(self._schema.model, name)
        return self._resolved[name]

    def __iter__(self) -> Iterator[str]:
        return iter(self._schema.properties)

    def __len__(self) -> int:
        return len(self._schema.properties)


def _bound_names(source: str) -> Dict[str, Any]:
    """The names a piece of generated source imports, bound as its body would see them.

    A cyclic type cannot be imported at module level -- the edge would close a cycle --
    so the generator writes the import inside the getter, or guards it with
    ``if TYPE_CHECKING:``. Either way the annotation names a type the module does not
    bind at runtime. The imports are read, not run: nothing is executed.
    """
    names: Dict[str, Any] = {}
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return names
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and not node.level:
            try:
                module = importlib.import_module(node.module)
            except ImportError:
                continue
            for alias in node.names:
                value = getattr(module, alias.name, None)
                if value is not None:
                    names.setdefault(alias.asname or alias.name, value)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                try:
                    names.setdefault(alias.asname or alias.name.split(".")[0], importlib.import_module(alias.name))
                except ImportError:
                    continue
    return names


def _resolve_declared_type(cls: type, name: str) -> Any:
    meta = TypeSchema.of(cls).properties.get(name)
    if meta is not None:
        attrs = (meta.attr,)
    else:
        # Generated getters rename reserved words with a trailing underscore
        # (``type`` -> ``type_``), a rename ``to_snake_case`` cannot express.
        attrs = (to_snake_case(name), to_snake_case(name) + "_")
    for attr in attrs:
        member = getattr(cls, attr, None)
        if member is None:
            continue
        target = member.fget if isinstance(member, property) else member
        declared = _return_hint(target)
        if declared is not None:
            return _unwrap_type(declared)
    if is_dataclass(cls):
        # A field is resolved on its own, never by resolving the class: one annotation
        # naming a name the module does not bind (a ``if TYPE_CHECKING:`` import) would
        # leave every other field of the class untyped -- a reader of 35 columns would
        # lose 35, not one.
        for declared in fields(cls):
            if declared.name in attrs:
                return _unwrap_type(_field_annotation(cls, declared))
    return None


def _return_hint(target: Any) -> Any:
    """A getter's return annotation, resolved where its own module does not bind it.

    A cyclic type is imported for a type checker, or inside the getter that returns it,
    because a module-level import would close the cycle; either way the module's own
    imports -- read, never run -- are the names ``get_type_hints`` is missing. One parse
    per module, cached, and only for the members a module does not bind.
    """
    try:
        return get_type_hints(target).get("return")
    except TypeError:
        # ``attr`` is not a function (a class constant sharing the OData name).
        return None
    except NameError:
        pass
    try:
        return get_type_hints(target, localns=_module_imports(target.__module__)).get("return")
    except (NameError, TypeError):
        return None


def _module_imports(module_name: str) -> Dict[str, Any]:
    """The names a module imports for itself, its ``TYPE_CHECKING`` block included.

    An annotation may name a type its module binds only for a type checker, and it is
    still the declaration a reader needs. Cached by module.
    """
    if module_name not in _module_names:
        try:
            source = inspect.getsource(importlib.import_module(module_name))
        except (OSError, TypeError, ImportError):
            source = ""
        _module_names[module_name] = _bound_names(source)
    return _module_names[module_name]


def _field_annotation(cls: type, declared: Any) -> Any:
    """One dataclass field's annotation, evaluated the way its own module spells it.

    The annotation is a string, and the module that wrote it is the one that imported the
    names in it -- not necessarily this class's module: a field declared on a base class is
    inherited, and the subclass's module need not import a name the base's annotation
    uses. So the class that declares the field is found first, and its module is asked.
    """
    annotation = declared.type
    if not isinstance(annotation, str):
        return annotation
    declaring = [base for base in cls.__mro__ if declared.name in base.__dict__.get("__annotations__", {})]
    for base in declaring or [cls]:
        scope = vars(importlib.import_module(base.__module__))
        for localns in (None, _module_imports(base.__module__)):
            try:
                return eval(annotation, scope, localns)  # noqa: S307 - generated annotations
            except (NameError, TypeError, SyntaxError, AttributeError):
                continue
    return None
