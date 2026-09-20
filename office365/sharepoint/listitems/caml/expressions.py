"""Typed CAML query expressions.

Build a ``<Where>`` clause from composable Python objects instead of raw CAML
strings. Every ``And``/``Or`` node holds **exactly two** children, so any
combination renders valid, binary-nested CAML (CAML forbids 3+ children):

    from office365.sharepoint.listitems.caml import Caml

    where = (
        Caml.text("Email").eq("support@google.com")
        .or_(Caml.text("Email").eq("plus@google.com"))
        .or_(Caml.text("Title").begins_with("[Google]"))
    )
    # identical alternatives:
    where = Caml.or_(a, b, c)   # variadic -> left-folded binary nesting
    where = a | b | c           # operators

Logical operators are ``&`` (And), ``|`` (Or), ``~`` (Not); the method forms
``.and_()/.or_()/.not_()`` read closer to CAML. Python's ``and``/``or``/``not``
cannot be used (they are keywords) and are rejected at runtime via ``__bool__``.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Iterable, Optional, TypeVar

from office365.sharepoint.listitems.caml.fields import FieldRef
from office365.sharepoint.listitems.caml.values import Value, ValueType, list_property
from office365.sharepoint.listitems.caml.values import month as _month
from office365.sharepoint.listitems.caml.values import now as _now
from office365.sharepoint.listitems.caml.values import today as _today
from office365.sharepoint.listitems.caml.values import user_id as _user_id

_T = TypeVar("_T")


class CamlExpr(ABC):
    """Base class for CAML query expressions."""

    @abstractmethod
    def to_xml(self) -> str:
        """Render this expression as CAML XML."""

    @property
    def field_refs(self) -> set[str]:
        """The field names referenced by this expression."""
        return set()

    def __and__(self, other: "CamlExpr") -> "And":
        return And(self, other)

    def __or__(self, other: "CamlExpr") -> "Or":
        return Or(self, other)

    def __invert__(self) -> "Not":
        return Not(self)

    def and_(self, other: "CamlExpr") -> "And":
        """Combine with ``other`` using ``<And>`` (same as ``&``)."""
        return And(self, other)

    def or_(self, other: "CamlExpr") -> "Or":
        """Combine with ``other`` using ``<Or>`` (same as ``|``)."""
        return Or(self, other)

    def not_(self) -> "Not":
        """Negate this expression (same as ``~``)."""
        return Not(self)

    def __bool__(self) -> bool:
        raise TypeError(
            "CAML expressions cannot be used with Python 'and'/'or'/'not'; "
            "use '&', '|', '~' or the .and_()/.or_()/.not_() methods"
        )


class Comparison(CamlExpr):
    """A comparison operator element, e.g. ``<Eq><FieldRef/><Value/></Eq>``."""

    def __init__(self, op: str, field: FieldRef, value: Value) -> None:
        self.op = op
        self.field = field
        self.value = value

    @property
    def field_refs(self) -> set[str]:
        return {self.field.name}

    def to_xml(self) -> str:
        return f"<{self.op}>{self.field.to_xml()}{self.value.to_xml()}</{self.op}>"


class IsNull(CamlExpr):
    """``<IsNull>`` (or ``<IsNotNull>``) element."""

    def __init__(self, field: FieldRef, negate: bool = False) -> None:
        self.field = field
        self.negate = negate

    @property
    def field_refs(self) -> set[str]:
        return {self.field.name}

    def to_xml(self) -> str:
        tag = "IsNotNull" if self.negate else "IsNull"
        return f"<{tag}>{self.field.to_xml()}</{tag}>"


class In(CamlExpr):
    """``<In>`` element over a list of values."""

    def __init__(self, field: FieldRef, values: Iterable[Value]) -> None:
        self.field = field
        self.values = list(values)

    @property
    def field_refs(self) -> set[str]:
        return {self.field.name}

    def to_xml(self) -> str:
        values = "".join(value.to_xml() for value in self.values)
        return f"<In>{self.field.to_xml()}<Values>{values}</Values></In>"


class Membership(CamlExpr):
    """``<Membership>`` element (e.g. ``Type="CurrentUserGroups"``)."""

    def __init__(self, field: FieldRef, type: str = "CurrentUserGroups") -> None:  # noqa: A002
        self.field = field
        self.type = type

    @property
    def field_refs(self) -> set[str]:
        return {self.field.name}

    def to_xml(self) -> str:
        from xml.sax.saxutils import quoteattr

        return f"<Membership Type={quoteattr(self.type)}>{self.field.to_xml()}</Membership>"


class DateRangesOverlap(CamlExpr):
    """``<DateRangesOverlap>`` element."""

    def __init__(self, field: FieldRef, value: Value) -> None:
        self.field = field
        self.value = value

    @property
    def field_refs(self) -> set[str]:
        return {self.field.name}

    def to_xml(self) -> str:
        return f"<DateRangesOverlap>{self.field.to_xml()}{self.value.to_xml()}</DateRangesOverlap>"


class _Binary(CamlExpr):
    """Base for the binary logical joins (``<And>``/``<Or>``)."""

    tag = ""

    def __init__(self, left: CamlExpr, right: CamlExpr) -> None:
        self.left = left
        self.right = right

    @property
    def field_refs(self) -> set[str]:
        return self.left.field_refs | self.right.field_refs

    def to_xml(self) -> str:
        return f"<{self.tag}>{self.left.to_xml()}{self.right.to_xml()}</{self.tag}>"


class And(_Binary):
    """``<And>`` — exactly two children (nest for 3+)."""

    tag = "And"


class Or(_Binary):
    """``<Or>`` — exactly two children (nest for 3+)."""

    tag = "Or"


class Not(CamlExpr):
    """``<Not>`` — exactly one child."""

    def __init__(self, child: CamlExpr) -> None:
        self.child = child

    @property
    def field_refs(self) -> set[str]:
        return self.child.field_refs

    def to_xml(self) -> str:
        return f"<Not>{self.child.to_xml()}</Not>"


def _fold(op: Callable[[CamlExpr, CamlExpr], _T], exprs: Iterable[CamlExpr]) -> _T:
    """Left-fold conditions into binary-nested nodes (``And(And(A,B),C)``)."""
    items = list(exprs)
    if not items:
        raise ValueError("at least one condition is required")
    result: Any = items[0]
    for item in items[1:]:
        result = op(result, item)
    return result  # type: ignore[no-any-return]


def _as_field_ref(field: Any) -> FieldRef:
    if isinstance(field, FieldRef):
        return field
    if isinstance(field, Field):
        return field.field_ref
    return FieldRef(str(field))


def _as_value(value: Any, value_type: Optional[ValueType] = None, **value_opts: Any) -> Value:
    if isinstance(value, Value):
        return value
    return Value(value, type=value_type, **value_opts)


class Field:
    """A typed field with fluent comparison methods.

    ``Caml.text("Status").eq("Active")`` renders ``<Eq>`` with ``Type='Text'``;
    ``Caml.lookup("Category").id().in_([2, 3])`` renders an ``<In>`` over
    ``Integer`` values with ``LookupId="TRUE"``.
    """

    def __init__(self, name: str, value_type: ValueType = ValueType.Text, *, lookup_id: bool = False) -> None:
        self.name = name
        self.value_type = value_type
        self.lookup_id = lookup_id

    @property
    def field_ref(self) -> FieldRef:
        return FieldRef(self.name, lookup_id=self.lookup_id)

    def id(self) -> "Field":
        """Treat this field as a lookup id (``LookupId="TRUE"``, ``Integer``)."""
        return Field(self.name, ValueType.Integer, lookup_id=True)

    def _compare(self, op: str, value: Any, **value_opts: Any) -> Comparison:
        return Comparison(op, self.field_ref, _as_value(value, self.value_type, **value_opts))

    def eq(self, value: Any, **value_opts: Any) -> Comparison:
        return self._compare("Eq", value, **value_opts)

    def neq(self, value: Any, **value_opts: Any) -> Comparison:
        return self._compare("Neq", value, **value_opts)

    def gt(self, value: Any, **value_opts: Any) -> Comparison:
        return self._compare("Gt", value, **value_opts)

    def geq(self, value: Any, **value_opts: Any) -> Comparison:
        return self._compare("Geq", value, **value_opts)

    def lt(self, value: Any, **value_opts: Any) -> Comparison:
        return self._compare("Lt", value, **value_opts)

    def leq(self, value: Any, **value_opts: Any) -> Comparison:
        return self._compare("Leq", value, **value_opts)

    def begins_with(self, value: Any, **value_opts: Any) -> Comparison:
        return self._compare("BeginsWith", value, **value_opts)

    def contains(self, value: Any, **value_opts: Any) -> Comparison:
        return self._compare("Contains", value, **value_opts)

    def not_contains(self, value: Any, **value_opts: Any) -> Comparison:
        return self._compare("NotContains", value, **value_opts)

    def includes(self, value: Any, **value_opts: Any) -> Comparison:
        return self._compare("Includes", value, **value_opts)

    def not_includes(self, value: Any, **value_opts: Any) -> Comparison:
        return self._compare("NotIncludes", value, **value_opts)

    def is_null(self) -> IsNull:
        return IsNull(self.field_ref)

    def is_not_null(self) -> IsNull:
        return IsNull(self.field_ref, negate=True)

    def in_(self, values: Iterable[Any]) -> In:
        return In(self.field_ref, [_as_value(value, self.value_type) for value in values])

    def eq_current_user(self) -> Comparison:
        """``<Eq><FieldRef LookupId='TRUE'/><Value><UserID/></Value></Eq>``."""
        return Comparison("Eq", self.field_ref, _user_id())

    def in_current_user_groups(self) -> Membership:
        """``<Membership Type='CurrentUserGroups'>``."""
        return Membership(self.field_ref, "CurrentUserGroups")


class Caml:
    """Factory namespace for CAML expressions and values."""

    # ── Special values ───────────────────────────────────────────
    now: Value = _now()
    today: Value = _today()
    month: Value = _month()
    user_id: Value = _user_id()
    list_property = staticmethod(list_property)

    # ── Typed fields ─────────────────────────────────────────────
    @staticmethod
    def field(name: str, value_type: ValueType = ValueType.Text, *, lookup_id: bool = False) -> Field:
        return Field(name, value_type, lookup_id=lookup_id)

    @staticmethod
    def text(name: str) -> Field:
        return Field(name, ValueType.Text)

    @staticmethod
    def number(name: str) -> Field:
        return Field(name, ValueType.Number)

    @staticmethod
    def integer(name: str) -> Field:
        return Field(name, ValueType.Integer)

    @staticmethod
    def date(name: str) -> Field:
        return Field(name, ValueType.DateTime)

    @staticmethod
    def boolean(name: str) -> Field:
        return Field(name, ValueType.Boolean)

    @staticmethod
    def lookup(name: str, *, id: bool = False) -> Field:  # noqa: A002
        return Field(name, ValueType.Integer, lookup_id=id)

    @staticmethod
    def user(name: str) -> Field:
        return Field(name, ValueType.Integer, lookup_id=True)

    # ── Comparisons (by field name, Field or FieldRef) ───────────
    @staticmethod
    def _compare(op: str, field: Any, value: Any, value_type: Optional[ValueType] = None) -> Comparison:
        return Comparison(op, _as_field_ref(field), _as_value(value, value_type))

    @staticmethod
    def eq(field: Any, value: Any) -> Comparison:
        return Caml._compare("Eq", field, value)

    @staticmethod
    def neq(field: Any, value: Any) -> Comparison:
        return Caml._compare("Neq", field, value)

    @staticmethod
    def gt(field: Any, value: Any) -> Comparison:
        return Caml._compare("Gt", field, value)

    @staticmethod
    def geq(field: Any, value: Any) -> Comparison:
        return Caml._compare("Geq", field, value)

    @staticmethod
    def lt(field: Any, value: Any) -> Comparison:
        return Caml._compare("Lt", field, value)

    @staticmethod
    def leq(field: Any, value: Any) -> Comparison:
        return Caml._compare("Leq", field, value)

    @staticmethod
    def begins_with(field: Any, value: Any) -> Comparison:
        return Caml._compare("BeginsWith", field, value)

    @staticmethod
    def contains(field: Any, value: Any) -> Comparison:
        return Caml._compare("Contains", field, value)

    @staticmethod
    def not_contains(field: Any, value: Any) -> Comparison:
        return Caml._compare("NotContains", field, value)

    @staticmethod
    def includes(field: Any, value: Any) -> Comparison:
        return Caml._compare("Includes", field, value)

    @staticmethod
    def not_includes(field: Any, value: Any) -> Comparison:
        return Caml._compare("NotIncludes", field, value)

    @staticmethod
    def is_null(field: Any) -> IsNull:
        return IsNull(_as_field_ref(field))

    @staticmethod
    def is_not_null(field: Any) -> IsNull:
        return IsNull(_as_field_ref(field), negate=True)

    @staticmethod
    def in_(field: Any, values: Iterable[Any], value_type: Optional[ValueType] = None) -> In:
        return In(_as_field_ref(field), [_as_value(value, value_type) for value in values])

    @staticmethod
    def membership(field: Any, type: str = "CurrentUserGroups") -> Membership:  # noqa: A002
        return Membership(_as_field_ref(field), type)

    @staticmethod
    def date_ranges_overlap(field: Any, value: Any) -> DateRangesOverlap:
        return DateRangesOverlap(_as_field_ref(field), _as_value(value))

    # ── Logical joins ────────────────────────────────────────────
    @staticmethod
    def and_(*exprs: CamlExpr) -> CamlExpr:
        return _fold(And, exprs)

    @staticmethod
    def or_(*exprs: CamlExpr) -> CamlExpr:
        return _fold(Or, exprs)

    @staticmethod
    def not_(expr: CamlExpr) -> Not:
        return Not(expr)
