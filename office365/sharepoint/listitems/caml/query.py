from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.sharepoint.listitems.collection_position import (
    ListItemCollectionPosition,
)
from office365.sharepoint.types.resource_path import ResourcePath
from office365.sharepoint.views.scope import ViewScope


@dataclass
class CamlQuery(ClientValue):
    """Specifies a Collaborative Application Markup Language (CAML) query on a list or joined lists.

    :type bool allowIncrementalResults: Specifies whether the incremental results can be returned.

    Args:
    list_item_collection_position (ListItemCollectionPosition): Specifies the information required to get the next page of data for the list view.
    view_xml (str): Specifies the XML schema that defines the list view.
    folder_server_relative_url (str or None): Specifies the server-relative URL of a list folder from which results are to be returned.
    dates_in_utc (bool): Specifies whether the query returns dates in Coordinated Universal Time (UTC) format.
    """

    DatesInUtc: bool = True
    ViewXml: str | None = None
    ListItemCollectionPosition: ListItemCollectionPosition | None = None
    FolderServerRelativeUrl: str | None = None
    AllowIncrementalResults: bool = True
    FolderServerRelativePath: ResourcePath | None = None

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
        qry_text = '<Where><Eq><FieldRef Name="FSObjType" /><Value Type="Integer">1</Value></Eq></Where>'
        return CamlQuery.parse(qry_text, ViewScope.DefaultValue)

    @staticmethod
    def create_all_files_query() -> CamlQuery:
        """Constructs a query to return file objects"""
        qry_text = '<Where><Eq><FieldRef Name="FSObjType" /><Value Type="Integer">0</Value></Eq></Where>'
        return CamlQuery.parse(qry_text, ViewScope.DefaultValue)

    def __repr__(self):
        return self.ViewXml or ""

    @property
    def entity_type_name(self):
        return "SP.CamlQuery"
