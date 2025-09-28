from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.sharepoint.listitems.collection_position import (
    ListItemCollectionPosition,
)
from office365.sharepoint.types.resource_path import ResourcePath
from office365.sharepoint.views.scope import ViewScope


class CamlQuery(ClientValue):

    def __init__(
        self,
        dates_in_utc: bool = True,
        view_xml: str = None,
        list_item_collection_position: ListItemCollectionPosition = None,
        folder_server_relative_url: str = None,
        allow_incremental_results: bool = True,
        folder_server_relative_path: ResourcePath = None,
    ):
        """
        Specifies a Collaborative Application Markup Language (CAML) query on a list or joined lists.

        :type bool allowIncrementalResults: Specifies whether the incremental results can be returned.
        :param ListItemCollectionPosition list_item_collection_position: Specifies the information required to
            get the next page of data for the list view.
        :param str view_xml: Specifies the XML schema that defines the list view.
        :param str or None folder_server_relative_url: Specifies the server-relative URL of a list folder from which
            results are to be returned.
        :param bool dates_in_utc: Specifies whether the query returns dates in Coordinated Universal Time (UTC) format.
        """
        super(CamlQuery, self).__init__()
        self.DatesInUtc = dates_in_utc
        self.FolderServerRelativeUrl = folder_server_relative_url
        self.AllowIncrementalResults = allow_incremental_results
        self.ViewXml = view_xml
        self.ListItemCollectionPosition = list_item_collection_position
        self.FolderServerRelativePath = folder_server_relative_path

    @staticmethod
    def parse(query_expr: str, scope: ViewScope = ViewScope.DefaultValue) -> CamlQuery:
        """
        Creates a CamlQuery object from a query expression

        :param str query_expr: Defines the query for a view.
        :param ViewScope scope: Specifies whether and how files and subfolders are included in a view.
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
        return self.ViewXml

    @property
    def entity_type_name(self):
        return "SP.CamlQuery"
