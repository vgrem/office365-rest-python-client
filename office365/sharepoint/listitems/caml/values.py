"""Typed CAML ``<Value>`` nodes.

A :class:`Value` renders a ``<Value Type='...'>...</Value>`` element, inferring
the OData value type from the Python value (``str`` -> ``Text``, ``int`` ->
``Integer``, ``bool`` -> ``Boolean``, ``datetime`` -> ``DateTime``) unless an
explicit type is given. Special values (``Now``/``Today``/``Month``/``UserID``/
``ListProperty``) render a child element instead of literal text.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, Optional
from xml.sax.saxutils import escape, quoteattr


class ValueType(str, Enum):
    """The ``Type`` attribute of a CAML ``<Value>`` element."""

    Text = "Text"
    Note = "Note"
    Integer = "Integer"
    Counter = "Counter"
    Number = "Number"
    Currency = "Currency"
    DateTime = "DateTime"
    Boolean = "Boolean"
    Lookup = "Lookup"
    User = "User"
    Choice = "Choice"
    URL = "URL"
    Guid = "Guid"
    Calculated = "Calculated"


def infer_value_type(value: Any) -> ValueType:
    """Infer the CAML ``ValueType`` from a Python value."""
    if isinstance(value, bool):  # bool before int (bool is an int subclass)
        return ValueType.Boolean
    if isinstance(value, int):
        return ValueType.Integer
    if isinstance(value, float):
        return ValueType.Number
    if isinstance(value, (datetime, date)):
        return ValueType.DateTime
    return ValueType.Text


class Value:
    """A CAML ``<Value>`` element."""

    def __init__(
        self,
        value: Any = None,
        *,
        type: Optional[ValueType | str] = None,  # noqa: A002
        include_time_value: bool = False,
        lookup_id: bool = False,
        child: Optional[str] = None,
    ) -> None:
        self._value = value
        self._type = ValueType(type) if isinstance(type, str) else type
        self._include_time_value = include_time_value
        self._lookup_id = lookup_id
        self._child = child  # raw child XML (e.g. "<Now/>")

    @property
    def value_type(self) -> ValueType:
        """The resolved ``ValueType`` (explicit type, else inferred)."""
        return self._type or infer_value_type(self._value)

    def to_xml(self) -> str:
        attrs = [f"Type={quoteattr(self.value_type.value)}"]
        if self._include_time_value:
            attrs.append('IncludeTimeValue="TRUE"')
        if self._lookup_id:
            attrs.append('LookupId="TRUE"')
        inner = self._child if self._child is not None else escape(self._format(self._value))
        return f"<Value {' '.join(attrs)}>{inner}</Value>"

    @staticmethod
    def _format(value: Any) -> str:
        if isinstance(value, bool):
            return "1" if value else "0"
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return str(value)


def now() -> Value:
    """A ``<Value Type='DateTime'><Now/></Value>`` node."""
    return Value(type=ValueType.DateTime, child="<Now/>")


def today() -> Value:
    """A ``<Value Type='DateTime'><Today/></Value>`` node."""
    return Value(type=ValueType.DateTime, child="<Today/>")


def month() -> Value:
    """A ``<Value Type='Integer'><Month/></Value>`` node."""
    return Value(type=ValueType.Integer, child="<Month/>")


def user_id() -> Value:
    """A ``<Value Type='Integer'><UserID/></Value>`` node."""
    return Value(type=ValueType.Integer, child="<UserID/>")


def list_property(name: str) -> Value:
    """A ``<Value><ListProperty Name='...'/></Value>`` node."""
    return Value(child=f"<ListProperty Name={quoteattr(name)}/>")
