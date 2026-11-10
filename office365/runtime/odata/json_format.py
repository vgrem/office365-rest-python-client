"""The OData JSON profile: one model, one payload, no per-entity code.

A *profile* is the shape the caller asked for. This one speaks OData JSON: it
decides what control information wraps a payload (:meth:`JsonProfile.wrap`) and
how a response is walked back into a model
(:meth:`JsonProfile.hydrate`).

Everything a specific service spells differently — JSON Light instead of
OData V4 — is a :class:`~office365.runtime.odata.dialect.JsonDialect` value, so
this class holds the *behaviour* and the dialect holds the *names*. That split
is why there is no ``isinstance`` check left in the response path: a new
dialect is a new table row, not a new branch.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Dict, Iterable, Iterator, Optional, Tuple, Union

from office365.runtime.converters.value import serialize_value
from office365.runtime.odata.dialect import BY_LEVEL, V4_NO_METADATA, JsonDialect
from office365.runtime.schema import TypeSchema
from office365.runtime.serialization import PropertyReceiver
from office365.runtime.types.odata_property import ODataPropertyMeta, request_version

if TYPE_CHECKING:
    from office365.runtime.odata.v3.metadata_level import ODataV3MetadataLevel
    from office365.runtime.odata.v4.metadata_level import ODataV4MetadataLevel


class JsonProfile:
    """An OData JSON profile: one dialect, selected by a metadata level.

    A profile is a level, not a subclass. Everything a level changes — the
    spelling of the payload, whether control information is written at all, and
    the media type that asks for it — is a row of
    :data:`~office365.runtime.odata.dialect.BY_LEVEL`, so the subclasses only
    name the level family they belong to and their fallback row. That is why
    :meth:`dialect` and :meth:`include_control_information` cannot disagree: an
    unrecognised level falls back to one row and both answers come from it.
    """

    _default_dialect: ClassVar[JsonDialect]
    """The row a level this family does not know falls back to."""

    addresses_version: ClassVar[bool] = True
    """Whether this profile addresses a version of the service root, and is gated by it."""

    def __init__(self, metadata_level: Optional[Union[ODataV3MetadataLevel, ODataV4MetadataLevel, str]] = None):
        """
        Initialize the OData JSON profile handler.

        Args:
            metadata_level: The level of metadata to include in responses.
                           Typical values are 'none', 'minimal', and 'full'.
                           Defaults to None which typically implies server defaults.
        """
        self.metadata_level = metadata_level

    @property
    def dialect(self) -> JsonDialect:
        """The dialect this profile speaks."""
        return BY_LEVEL.get(self.metadata_level, self._default_dialect)

    @property
    def media_type(self) -> str:
        """str: Gets the official media type for this profile (e.g., 'application/json')"""
        level = getattr(self.metadata_level, "value", self.metadata_level)
        return f"application/json;{self.dialect.media_type_parameter}={level}{self._media_type_options}"

    @property
    def _media_type_options(self) -> str:
        """Extra media-type parameters this family appends after the level."""
        return ""

    @property
    def include_control_information(self) -> bool:
        """
        bool: Determines whether control information should be included in payload

        Control information includes annotations and other OData-specific metadata
        that guides client behavior but isn't part of the actual entity data.
        """
        return self.dialect.control_information

    @property
    def collection_delta(self) -> str:
        """str: The JSON property name used for delta/differential updates"""
        return self.dialect.collection_delta

    def wrap(self, obj: Any, payload: Any) -> Any:
        """Attach this dialect's control information to an outbound payload.

        A post-transform rather than an envelope state machine: JSON documents
        are bounded, and the unbounded one (a raw MIME message) travels as bytes
        through a codec, never as a profile payload.

        Args:
            obj: The value being serialized (its ``entity_type_name`` is declared)
            payload: The serialized columns

        Returns:
            The payload, with control information added when the dialect and the
            metadata level ask for it
        """
        # A type is declared only when the value could name one, and written only
        # when the level carries control information; the envelope below is the
        # dialect's spelling of a collection either way.
        name: Optional[str] = getattr(obj, "entity_type_name", None)
        if not self.include_control_information:
            name = None
        if isinstance(payload, list):
            # JSON Light names a collection payload; an unwrapped dialect sends
            # the bare array, so there is no envelope to spell.
            if self.dialect.container is None:
                return payload
            wrapped: dict[str, Any] = {self.dialect.collection: payload}
            if name is not None:
                wrapped[self.dialect.type_marker] = {"type": name}
            return wrapped
        if payload and name is not None:
            payload[self.dialect.type_marker] = {"type": name} if self.dialect.type_wrapped else "#" + name
        return payload

    def includes(self, owner: Any, declared: Optional[ODataPropertyMeta], name: str, changed: bool) -> bool:
        """Whether a property of ``owner`` enters a payload this profile spells.

        ``name`` is the property's *spelled* name (the OData one), whether ``owner`` holds
        it as a wire key or declares it on a Python attribute. A request carries what its
        sender changed (or what a type always sends) and never what the service assigns: a
        read-only field is what a response carries. A profile that spells something else,
        such as a comparable form, decides for itself.
        """
        return changed and not (declared is not None and declared.readonly)

    def scoped(self, model: Any, *, only: Optional[Iterable[str]] = None, without: Iterable[str] = ()) -> JsonProfile:
        """This profile, narrowed for one model to some of its properties.

        ``only`` and ``without`` name Python attributes of ``model``, resolved through its
        declarations so a misspelling raises. The narrowing applies to ``model`` itself,
        never to a nested value that happens to share an OData name (an ``EmailAddress``
        keeps its ``name`` when a contact leaves out its own).
        """
        return ScopedProfile(self, model, only, without)

    def refine(self, spelled: Dict[str, Any], declarations: Iterable[ODataPropertyMeta]) -> Dict[str, Any]:
        """The last word on the fields of one value, after each was spelled.

        ``declarations`` are the ``@odata`` rows of the value's type. A request leaves
        the fields as they were spelled.
        """
        return spelled

    def serialize(self, carrier: Any) -> Any:
        """Spell one carrier -- an entity or a value -- as this profile's payload.

        The carrier states what it holds, under the names its type declares; everything else
        is the profile's: which fields a payload carries (:meth:`includes`), how their names
        are spelled (a request addresses a root, which renames and gates them), and the
        control information around the result (:meth:`wrap`). This is the write half of
        :meth:`hydrate` -- ``x.hydrate(y.to_json())`` reads back what ``y.to_json()`` wrote.
        """
        schema = TypeSchema.of(carrier)
        version = request_version(getattr(carrier, "context", None)) if self.addresses_version else None
        spelled: Dict[str, Any] = {}
        for name, value, changed in carrier:
            if self.includes(carrier, schema.properties.get(name), name, changed):
                spelled[schema.wire_name(name, version)] = serialize_value(value, self)
        return self.wrap(carrier, self.refine(spelled, schema.properties.values()))

    def build_payload(self, source: Any) -> Any:
        """Serialize a query's parameters into the body the service will read.

        Parameters are not a document: a ``None`` parameter means "not
        provided" and is dropped, and no column is bookkeeping, so nothing is
        filtered here beyond that. Nested values carry this profile, so a
        collection of values is spelled exactly as its dialect spells it.

        Args:
            source: The parameters (a value, a container, or ``None``)

        Returns:
            The JSON-ready body
        """
        return {} if source is None else serialize_value(source, self, skip_none=True)

    def hydrate(
        self, target: PropertyReceiver, payload: Any, wrapper: Optional[str] = None, persist_changes: bool = False
    ) -> None:
        """Ingest ``payload`` into ``target`` through this dialect.

        Args:
            target: The ``ClientObject``/``ClientValue``/``ClientResult`` to fill
            payload: The decoded JSON body
            wrapper: Name of a service operation/function wrapper key, if the
                dialect wraps its result (JSON Light does, OData V4 does not)
            persist_changes: Mark what was read as a change, for a payload that is
                read in order to be written elsewhere (a draft): a response is
                ingested as-is, a draft is ingested as intent
        """
        if not payload or not isinstance(payload, (dict, list)):
            return
        for name, value in self.iter_payload(payload, wrapper):
            target.set_property(str(name), value, persist_changes)

    def iter_payload(self, payload: Any, wrapper: Optional[str] = None) -> Iterator[Tuple[Union[str, int], Any]]:
        """Yield ``(property name, value)`` pairs from a decoded JSON body.

        A collection arrives in one of four shapes and each is unwrapped here:
        a page (``{collection: [...], next: link}``), a bare array, an entity
        object, or a primitive value.

        Args:
            payload: The decoded JSON body
            wrapper: Name of the service operation/function wrapper key

        Yields:
            Property name (or list index) and its raw value
        """
        if isinstance(payload, dict):
            if self.dialect.container:
                payload = payload.get(self.dialect.container, payload)
            if wrapper:
                payload = payload.get(wrapper, payload)
            if isinstance(payload, dict):
                items = payload.get(self.dialect.collection)
                if isinstance(items, list):
                    next_link_url = payload.get(self.dialect.collection_next)
                    payload = items
                    if next_link_url:
                        yield "__nextLinkUrl", next_link_url

        if isinstance(payload, list):
            for index, item in enumerate(payload):
                yield index, dict(self.iter_payload(item)) if isinstance(item, dict) else item
        elif isinstance(payload, dict):
            for name, value in payload.items():
                yield from self.iter_property(name, value)
        else:
            yield "__value", payload

    def iter_property(self, name: str, value: Any) -> Iterator[Tuple[str, Any]]:
        """Yield one property of a JSON object, dropping or renaming control information."""
        if not self.dialect.dropped(name, value):
            yield name, dict(self.iter_payload(value)) if isinstance(value, dict) else value
            return
        alias = self.dialect.alias(name)
        if alias is not None and isinstance(value, str):
            yield alias, value


class ScopedProfile(JsonProfile):
    """A profile that leaves some properties of one model out of what it spells."""

    def __init__(
        self, base: JsonProfile, model: Any, only: Optional[Iterable[str]] = None, without: Iterable[str] = ()
    ) -> None:
        super().__init__(base.metadata_level)
        self._base = base
        self._model = model
        schema = TypeSchema.of(model)
        self._only = None if only is None else frozenset(schema.name_of(attr) for attr in only)
        self._without = frozenset(schema.name_of(attr) for attr in without)
        # ``refine`` is not told which type it is refining, so the narrowing is applied to
        # the one call that was handed exactly this model's own declarations. That is what
        # keeps a nested value sharing an OData name untouched.
        self._own = frozenset(map(id, schema.properties.values()))

    @property
    def dialect(self) -> JsonDialect:
        return self._base.dialect

    @property
    def media_type(self) -> str:
        return self._base.media_type

    def includes(self, owner: Any, declared: Optional[ODataPropertyMeta], name: str, changed: bool) -> bool:
        if isinstance(owner, self._model) and (
            name in self._without or (self._only is not None and name not in self._only)
        ):
            return False
        return self._base.includes(owner, declared, name, changed)

    def refine(self, spelled: Dict[str, Any], declarations: Iterable[ODataPropertyMeta]) -> Dict[str, Any]:
        form = self._base.refine(spelled, declarations)
        if frozenset(map(id, declarations)) != self._own:
            return form
        # Last word, after the base profile refined: a rule that fills a field in from a
        # sibling must not resurrect one this scope left out.
        return {
            name: value
            for name, value in form.items()
            if name not in self._without and (self._only is None or name in self._only)
        }

    def wrap(self, obj: Any, payload: Any) -> Any:
        return self._base.wrap(obj, payload)


class HeldProfile(JsonProfile):
    """Spells a carrier as the model holds it, and reads one back the same way.

    No policy: every field the carrier holds is spelled, including one the service assigns,
    and nothing is written around the result -- the dialect carries no control information.
    That is what both verbs fall back to when the caller names no profile.
    """

    _default_dialect = V4_NO_METADATA

    def __init__(self) -> None:
        super().__init__("none")

    addresses_version = False

    def includes(self, owner: Any, declared: Optional[ODataPropertyMeta], name: str, changed: bool) -> bool:
        """Every field: what a carrier holds is what it says."""
        return True


HELD = HeldProfile()
"""The profile that spells and reads a carrier as the model holds it: see :class:`HeldProfile`."""


ODataJsonFormat = JsonProfile
"""Backwards-compatible name for :class:`JsonProfile`."""
