from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, ClassVar, Dict, Iterator, Optional, Tuple

from typing_extensions import Self, dataclass_transform

from office365.runtime.converters.value import declared_type, deserialize_value
from office365.runtime.odata.json_format import HELD, JsonProfile
from office365.runtime.schema import EMPTY, TypeSchema


def _render(self: "ClientValue") -> str:
    """Bounded, side-effect-free rendering shared by ``str`` and ``repr``."""
    from office365.runtime.display import describe

    return describe(self)


def _is_content(value: Any) -> bool:
    """Whether a field of a value is content.

    A ``None``, ``datetime.min`` or empty collection is what a dataclass default
    looks like before the model fills it in, and a nested value with nothing in it
    is the same fact one level down, so none of them is content.
    """
    from office365.runtime.client_value_collection import ClientValueCollection

    if value is None:
        return False
    if isinstance(value, datetime) and value == datetime.min:
        return False
    if isinstance(value, ClientValueCollection) and len(value) == 0:
        return False
    if isinstance(value, ClientValue):
        return any(_is_content(member) for member in vars(value).values())
    return True


@dataclass_transform()
class ClientValue:
    """Represent complex type.
    Complex types consist of a list of properties with no key, and can therefore only exist as properties of a
    containing entity or as a temporary value
    """

    #: What this value declares, read in ``__init_subclass__`` when the class is complete.
    _schema: ClassVar[TypeSchema] = EMPTY
    #: The OData name this value declares (``"microsoft.graph.DateTimeTimeZone"``).
    _odata_type_name: ClassVar[Optional[str]] = None

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Read the class once it is complete: its fields, then the facts they state.

        The order is the whole point. ``dataclass`` is what gives the class its fields
        -- their names, their defaults and the ``__init__`` a caller writes keywords
        against -- and the schema is read from those fields, so it has to run second.
        Nothing above the class can still add a field by now, which is why this is the
        first moment the schema can answer for the whole class; a decorator above it
        (``@key``, ``@version``, ``@limit``) states a class-level fact and rebuilds
        through ``TypeSchema.rebuild``.

        ``dataclass_transform`` on the class is what tells a type checker that this
        hook, not a literal ``@dataclass`` above each subclass, is what gives the
        class its constructor: without it every value looks like a class with no
        arguments.
        """
        super().__init_subclass__(**kwargs)
        dataclass(cls, repr=False)
        # ``repr=False`` declines to install a rendering, and a rendering only wins against a
        # later ``dataclass`` -- a subclass of this one that still applies its own -- if the
        # class already carries it. Pin the bounded rendering a plain value would inherit
        # anyway; a class that states (or inherits) another one keeps it.
        if cls.__dict__.get("__repr__") is None and cls.__repr__ is ClientValue.__repr__:
            cls.__repr__ = _render
        cls._schema = TypeSchema.build(cls)

    def __str__(self) -> str:
        return _render(self)

    def __repr__(self) -> str:
        return _render(self)

    def __format__(self, format_spec: str) -> str:
        return format(str(self), format_spec)

    def hydrate(self, payload: Any, profile: Optional[JsonProfile] = None) -> Self:
        """Read this value's content from a payload: the mirror of :meth:`to_json`.

        ``profile=None`` is the spelling :meth:`to_json` writes with no profile, so a value
        round-trips through it; a wire payload needs its own profile (see
        :meth:`ClientObject.hydrate`). Returns this value, so ``Cls().hydrate(payload)`` chains.
        """
        (profile or HELD).hydrate(self, payload, persist_changes=True)
        return self

    def set_property(self, name: str | int, value: Any, persist_changes: bool = True) -> Self:
        spelled = str(name)
        key = self._storage_key(spelled)
        if value is None:
            setattr(self, key, None)
            return self
        declared = declared_type(type(self), spelled)
        setattr(self, key, deserialize_value(declared, value, getattr(self, key, None), persist_changes))
        return self

    def _storage_key(self, name: str) -> str:
        """The attribute that holds ``name``, which a declaration may rename.

        A value keeps its fields as attributes, while a payload spells them the OData
        way, so the two sides meet at the declaration: ``UserIdInfo`` holds ``NameId``
        in ``name_id``. ``to_json`` already reads the attribute and writes the declared
        name; this is the same rule in the other direction. An undeclared name is held
        under its own spelling, which is what makes an undeclared value work at all.
        """
        declared = TypeSchema.of(type(self)).properties.get(name)
        return declared.attr if declared is not None else name

    def get_property(self, name: str, default_value: Any = None) -> Any:
        """Gets a property value, or ``default_value`` when the property is unset.

        Mirrors :meth:`ClientObject.get_property` so the same call works on a
        ClientValue (e.g. ``draft.body.get_property("content", "")``).

        Args:
            name: Name of the property to retrieve
            default_value: Value to return when the property is missing
        """
        return getattr(self, self._storage_key(name), default_value)

    def __iter__(self) -> Iterator[Tuple[str, Any, bool]]:
        """The fields this value holds: the OData name each is sent under, its value, and
        whether a sender states it.

        A ``_``-prefixed attribute is this client's own state (a form digest's age, an
        expression AST) and a dataclass default the model never filled is not content
        (:func:`_is_content`), so neither is a field. A key no column declares is an
        endpoint-specific field whatever it holds: ``null`` is how an open type removes an
        entry. A value tracks no changes, so everything it holds is stated.

        Yields:
            The declared name, the value, and whether the sender states it
        """
        schema = self._schema
        for attr, value in vars(self).items():
            declared = schema.declared(attr)
            if attr.startswith("_") or (declared is not None and not _is_content(value)):
                continue
            yield (declared.name if declared is not None else attr), value, True

    def to_json(self, profile: Optional[JsonProfile] = None) -> Dict[str, Any]:
        """Serialize this value as a payload: ``profile`` spells it, ``None`` spells it as held.

        Nothing is decided here -- see
        :meth:`~office365.runtime.odata.json_format.JsonProfile.serialize`; what this value
        states is what it yields when iterated.

        Args:
            profile: The profile that spells the payload. ``None`` keeps the value as the
                model holds it, including the fields a request would leave out.

        Returns:
            Dictionary representing the JSON-serialized value (a collection value
            overrides this to answer the list of its members)
        """
        return (profile or HELD).serialize(self)

    @property
    def entity_type_name(self) -> Optional[str]:
        """The server-side type name for this client value.

        Returns:
            The declared OData type name, or ``None`` when the value declares none.
        """
        return self._odata_type_name
