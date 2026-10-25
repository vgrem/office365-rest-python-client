from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar, Dict, Iterator, Optional, Tuple

from typing_extensions import Self

from office365.runtime.converters.value import coerce_value, declared_type, serialize_value
from office365.runtime.odata.json_format import JsonProfile, as_held
from office365.runtime.types.odata_property import field_declarations


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
    #: The OData name this value declares (``"microsoft.graph.DateTimeTimeZone"``).
    _odata_type_name: ClassVar[Optional[str]] = None

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # ``@dataclass`` generates a ``__repr__`` unless one is already present
        # in the class ``__dict__``, which would shadow the bounded rendering
        # inherited from the nearest ancestor — ``_render`` for a plain value,
        # the list/table preview for a collection subclass. Subclasses run
        # ``__init_subclass__`` before the decorator is applied, so seeding the
        # nearest ancestor's method here keeps dataclass-backed values
        # consistent with every other ClientValue (and with domain overrides
        # that define their own ``__repr__``).
        if "__repr__" not in cls.__dict__:
            for klass in cls.__mro__[1:]:
                if "__repr__" in klass.__dict__:
                    cls.__repr__ = klass.__dict__["__repr__"]
                    break

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
        key = str(name)
        if value is None:
            setattr(self, key, None)
            return self
        setattr(
            self, key, coerce_value(declared_type(type(self), key), value, getattr(self, key, None), persist_changes)
        )
        return self

    def get_property(self, name: str, default_value: Any = None) -> Any:
        """Gets a property value, or ``default_value`` when the property is unset.

        Mirrors :meth:`ClientObject.get_property` so the same call works on a
        ClientValue (e.g. ``draft.body.get_property("content", "")``).

        Args:
            name: Name of the property to retrieve
            default_value: Value to return when the property is missing
        """
        return getattr(self, name, default_value)

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
                if not any(v is not None for v in vars(val).values()):
                    return False
            return True

        # ``__``-prefixed names are response bookkeeping, not fields of the value.
        # A declared field may also rename itself and declare who owns its value; a
        # read-only field is what a response carries and a request must not.
        by_attr = field_declarations(type(self))
        result: Dict[str, Any] = {}
        for attr, value in self:
            meta = by_attr.get(attr)
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
        return profile.wrap(self, profile.refine(result, by_attr.values()))

    @classmethod
    def odata_name(cls, attr: str) -> str:
        """The OData name of a declared field, given its Python attribute name.

        The mirror of :meth:`ClientObject.odata_name`, so a profile that narrows a type can
        resolve a name without knowing which of the two kinds of model it was handed.

        Raises:
            AttributeError: when the attribute carries no declaration, naming the
                declared attributes so a typo fails here rather than as ``None``
                further down the read path.
        """
        declared = field_declarations(cls)
        meta = declared.get(attr)
        if meta is not None:
            return meta.name
        raise AttributeError(
            f"{cls.__name__}.{attr} is not a declared property; declared: {', '.join(sorted(declared))}"
        )

    @property
    def entity_type_name(self) -> Optional[str]:
        """The server-side type name for this client value.

        Returns:
            The declared OData type name, or ``None`` when the value declares none.
        """
        return self._odata_type_name
