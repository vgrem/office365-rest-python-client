from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar, Dict, Iterator, Optional, Tuple

from typing_extensions import Self

from office365.runtime.converters.value import coerce_value, declared_type, serialize_value
from office365.runtime.odata.json_format import JsonProfile, as_held
from office365.runtime.schema import EMPTY, TypeSchema


def _render(self: "ClientValue") -> str:
    """Bounded, side-effect-free rendering shared by ``str`` and ``repr``."""
    from office365.runtime.display import describe

    return describe(self)


class ClientValue:
    """Represent complex type.
    Complex types consist of a list of properties with no key, and can therefore only exist as properties of a
    containing entity or as a temporary value
    """

    _is_client_value: bool = True
    #: What this value declares, built by ``@value`` when the class is declared.
    _schema: ClassVar[TypeSchema] = EMPTY
    #: The OData name this value declares (``"microsoft.graph.DateTimeTimeZone"``).
    _odata_type_name: ClassVar[Optional[str]] = None

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
        (profile or as_held()).hydrate(self, payload, persist_changes=True)
        return self

    def set_property(self, name: str | int, value: Any, persist_changes: bool = True) -> Self:
        spelled = str(name)
        key = self._storage_key(spelled)
        if value is None:
            setattr(self, key, None)
            return self
        declared = declared_type(type(self), spelled)
        setattr(self, key, coerce_value(declared, value, getattr(self, key, None), persist_changes))
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

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for n, v in vars(self).items():
            yield n, v

    def to_json(self, profile: Optional[JsonProfile] = None) -> Dict[str, Any]:
        """Serializes the ClientValue to JSON format.

        Args:
            profile: The profile that spells the payload. ``None`` keeps the value as the
                model holds it, including the fields a request would leave out.

        Returns:
            Dictionary representing the JSON-serialized value (a collection value
            overrides this to answer the list of its members)
        """

        def _is_valid_value(val):
            from office365.runtime.client_value_collection import ClientValueCollection

            if val is None:
                return False
            elif isinstance(val, datetime) and val == datetime.min:
                return False
            elif isinstance(val, ClientValueCollection) and len(val) == 0:
                return False
            elif isinstance(val, ClientValue):
                # A nested value with nothing to send (all members unset or empty) is omitted.
                if not any(_is_valid_value(v) for v in vars(val).values()):
                    return False
            return True

        # ``__``-prefixed names are response bookkeeping, not fields of the value.
        # A declared field may also rename itself and declare who owns its value; a
        # read-only field is what a response carries and a request must not.
        schema = TypeSchema.of(type(self))
        result: Dict[str, Any] = {}
        for attr, value in self:
            meta = schema.declared(attr)
            if attr.startswith("__") or not _is_valid_value(value):
                continue
            spelled = meta.name if meta is not None else attr
            if profile is not None and (
                (meta is not None and meta.readonly) or not profile.includes(self, meta, spelled, True)
            ):
                continue
            result[spelled] = serialize_value(value, profile)
        if profile is None:
            return result
        return profile.wrap(self, profile.refine(result, schema.properties.values()))

    @property
    def entity_type_name(self) -> Optional[str]:
        """The server-side type name for this client value.

        Returns:
            The declared OData type name, or ``None`` when the value declares none.
        """
        return self._odata_type_name
