"""Typed CAML query builder.

Build CAML ``ViewXml`` from composable Python objects instead of raw strings::

    from office365.sharepoint.listitems.caml import Caml, CamlQuery

    query = (
        CamlQuery.builder()
        .where(Caml.text("Status").eq("Active"))
        .order_by("Created", ascending=False)
        .row_limit(2000)
        .build()
    )
"""

from office365.sharepoint.listitems.caml.builder import QueryBuilder
from office365.sharepoint.listitems.caml.expressions import Caml, CamlExpr, Field
from office365.sharepoint.listitems.caml.fields import FieldRef
from office365.sharepoint.listitems.caml.query import CamlQuery
from office365.sharepoint.listitems.caml.values import Value, ValueType

__all__ = [
    "Caml",
    "CamlExpr",
    "CamlQuery",
    "Field",
    "FieldRef",
    "QueryBuilder",
    "Value",
    "ValueType",
]
