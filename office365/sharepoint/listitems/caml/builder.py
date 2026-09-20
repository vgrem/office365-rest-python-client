"""Fluent builder for the CAML ``<View>`` document.

Assembles ``ViewFields``/``Where``/``GroupBy``/``OrderBy``/``RowLimit``/``Scope``
into a ``ViewXml`` string (or a :class:`CamlQuery`):

    from office365.sharepoint.listitems.caml import Caml, CamlQuery
    from office365.sharepoint.views.scope import ViewScope

    query = (CamlQuery.builder()
        .where(Caml.text("Status").eq("Active"))
        .order_by("Created", ascending=False)
        .row_limit(2000)
        .scope(ViewScope.RecursiveAll)
        .build())
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional
from xml.sax.saxutils import quoteattr

from typing_extensions import Self

from office365.sharepoint.listitems.caml.expressions import And, CamlExpr, _as_field_ref, _fold
from office365.sharepoint.listitems.caml.fields import FieldRef
from office365.sharepoint.views.scope import ViewScope

if TYPE_CHECKING:
    from office365.sharepoint.listitems.caml.query import CamlQuery


class QueryBuilder:
    """Fluent builder that renders the CAML ``<View>`` element."""

    def __init__(self) -> None:
        self._where: Optional[CamlExpr] = None
        self._order_by: list[FieldRef] = []
        self._group_by: list[FieldRef] = []
        self._view_fields: list[FieldRef] = []
        self._row_limit: Optional[int] = None
        self._paged = True
        self._scope: ViewScope = ViewScope.DefaultValue

    def where(self, *conditions: CamlExpr) -> Self:
        """Set the ``<Where>`` filter (multiple conditions are combined with ``<And>``)."""
        if conditions:
            self._where = _fold(And, conditions)
        return self

    def order_by(self, *fields: Any, ascending: bool = True) -> Self:
        """Add one or more ``<OrderBy>`` fields (call again to append)."""
        for field in fields:
            ref = _as_field_ref(field)
            self._order_by.append(ref if ref.ascending is not None else ref._copy(ascending=ascending))
        return self

    def group_by(self, field: Any, *, collapse: bool = True) -> Self:
        """Add a ``<GroupBy>`` field."""
        ref = _as_field_ref(field)
        self._group_by.append(ref if ref.collapse is not None else ref._copy(collapse=collapse))
        return self

    def view_fields(self, *names: Any) -> Self:
        """Add ``<ViewFields>`` entries (a ``str``, ``Field`` or ``FieldRef``)."""
        self._view_fields.extend(_as_field_ref(name) for name in names)
        return self

    def row_limit(self, top: int, *, paged: bool = True) -> Self:
        """Set ``<RowLimit>`` (``Paged="TRUE"`` by default)."""
        self._row_limit = top
        self._paged = paged
        return self

    def scope(self, scope: ViewScope) -> Self:
        """Set the ``Scope`` attribute of ``<View>``."""
        self._scope = scope
        return self

    @property
    def is_paged(self) -> bool:
        """Whether the query enables server-driven paging (``RowLimit Paged="TRUE"``)."""
        return self._row_limit is not None and self._paged

    @property
    def field_refs(self) -> set[str]:
        """Fields the query filters or sorts on (``ViewFields`` are excluded)."""
        names: set[str] = set()
        if self._where is not None:
            names |= self._where.field_refs
        for ref in (*self._order_by, *self._group_by):
            names.add(ref.name)
        return names

    def to_xml(self) -> str:
        """Render the CAML ``<View>`` document."""
        scope = self._scope.value if isinstance(self._scope, ViewScope) else str(self._scope)
        parts = [f"<View Scope={quoteattr(scope)}>"]
        if self._view_fields:
            parts.append("<ViewFields>" + "".join(ref.to_xml() for ref in self._view_fields) + "</ViewFields>")
        query = self._query_xml()
        if query:
            parts.append(query)
        if self._row_limit is not None:
            paged = ' Paged="TRUE"' if self._paged else ""
            parts.append(f"<RowLimit{paged}>{self._row_limit}</RowLimit>")
        parts.append("</View>")
        return "".join(parts)

    def _query_xml(self) -> str:
        query: list[str] = []
        if self._where is not None:
            query.append(f"<Where>{self._where.to_xml()}</Where>")
        if self._group_by:
            query.append("<GroupBy>" + "".join(ref.to_xml() for ref in self._group_by) + "</GroupBy>")
        if self._order_by:
            query.append("<OrderBy>" + "".join(ref.to_xml() for ref in self._order_by) + "</OrderBy>")
        return "<Query>" + "".join(query) + "</Query>" if query else ""

    def build(self) -> "CamlQuery":
        """Build a :class:`CamlQuery` (raw ``ViewXml`` + the expression AST)."""
        from office365.sharepoint.listitems.caml.query import CamlQuery

        query = CamlQuery()
        query.ViewXml = self.to_xml()
        query._expr = self
        return query

    def __repr__(self) -> str:
        return self.to_xml()
