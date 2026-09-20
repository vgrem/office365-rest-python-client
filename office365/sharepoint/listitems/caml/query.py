from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterator, Tuple

from office365.runtime.client_value import ClientValue
from office365.sharepoint.fields.builtin_field_name import SPBuiltInFieldName
from office365.sharepoint.listitems.collection_position import (
    ListItemCollectionPosition,
)
from office365.sharepoint.types.resource_path import ResourcePath
from office365.sharepoint.views.scope import ViewScope

if TYPE_CHECKING:
    from office365.sharepoint.listitems.caml.builder import QueryBuilder

_FIELD_REF_RE = re.compile(r"<FieldRef\s+Name=['\"]([^'\"]+)['\"]", re.IGNORECASE)


@dataclass
class CamlQuery(ClientValue):
    """Specifies a Collaborative Application Markup Language (CAML) query on a list or joined lists.

    Args:
    allow_incremental_results (bool): Specifies whether the incremental results can be returned.
    list_item_collection_position (ListItemCollectionPosition): Specifies the information required to get the next page
        of data for the list view.
    view_xml (str): Specifies the XML schema that defines the list view.
    folder_server_relative_url (str or None): Specifies the server-relative URL of a list folder from which results are
        to be returned.
    dates_in_utc (bool): Specifies whether the query returns dates in Coordinated Universal Time (UTC) format.
    """

    DatesInUtc: bool = True
    ViewXml: str | None = None
    ListItemCollectionPosition: ListItemCollectionPosition | None = None
    FolderServerRelativeUrl: str | None = None
    AllowIncrementalResults: bool = True
    FolderServerRelativePath: ResourcePath | None = None

    def __post_init__(self) -> None:
        # The expression AST (set by QueryBuilder.build()); not serialized.
        self._expr: "QueryBuilder | None" = None

    @staticmethod
    def builder() -> "QueryBuilder":
        """A fluent builder for this query (``ViewFields``/``Where``/``OrderBy``/...)."""
        from office365.sharepoint.listitems.caml.builder import QueryBuilder

        return QueryBuilder()

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        """Yield serializable properties (skips private attrs such as the AST)."""
        for name, value in vars(self).items():
            if not name.startswith("_"):
                yield name, value

    @staticmethod
    def parse(query_expr: str, scope: ViewScope = ViewScope.DefaultValue) -> CamlQuery:
        """Creates a CamlQuery object from a query expression

        Args:
            query_expr (str): Defines the query for a view.
            scope (ViewScope): Specifies whether and how files and subfolders are included in a view.
        """
        qry = CamlQuery()
        qry.ViewXml = f'<View Scope="{scope}"><Query>{query_expr}</Query></View>'
        return qry

    @staticmethod
    def create_all_items_query() -> CamlQuery:
        """Constructs a query"""
        return CamlQuery.parse("", ViewScope.RecursiveAll)

    @staticmethod
    def create_all_folders_query() -> CamlQuery:
        """Constructs a query to return folder objects"""
        qry_text = (
            f'<Where><Eq><FieldRef Name="{SPBuiltInFieldName.FSObjType}" /><Value Type="Integer">1</Value></Eq></Where>'
        )
        return CamlQuery.parse(qry_text, ViewScope.DefaultValue)

    @staticmethod
    def create_all_files_query() -> CamlQuery:
        """Constructs a query to return file objects"""
        qry_text = (
            f'<Where><Eq><FieldRef Name="{SPBuiltInFieldName.FSObjType}" /><Value Type="Integer">0</Value></Eq></Where>'
        )
        return CamlQuery.parse(qry_text, ViewScope.DefaultValue)

    @property
    def is_paged(self) -> bool:
        """Whether the query uses server-driven paging (``RowLimit Paged='TRUE'``)."""
        if self._expr is not None:
            return self._expr.is_paged
        xml = self.ViewXml or ""
        return "Paged='TRUE'" in xml or 'Paged="TRUE"' in xml

    @property
    def field_refs(self) -> set[str]:
        """The field names referenced by the query.

        Uses the expression AST when the query was produced by the builder, else
        falls back to scanning the raw ``ViewXml``.
        """
        if self._expr is not None:
            return self._expr.field_refs
        return {match.group(1) for match in _FIELD_REF_RE.finditer(self.ViewXml or "")}

    def __repr__(self):
        return self.ViewXml or ""

    @property
    def entity_type_name(self):
        return "SP.CamlQuery"
