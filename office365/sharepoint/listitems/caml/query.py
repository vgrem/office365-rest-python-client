from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.sharepoint.listitems.collection_position import (
    ListItemCollectionPosition,
)
from office365.sharepoint.views.scope import ViewScope


class WhereElement:
    """Used within the context of a query to specify a filter."""

    def __str__(self):
        return "<Where></Where>"


class OrderByElement:
    """Determines the sort order for a query"""

    def __str__(self):
        return "<OrderBy></OrderBy>"


class GroupByElement:
    """Contains a Group By section for grouping the data returned through a query in a list view."""

    def __str__(self):
        return "<GroupBy></GroupBy>"


class QueryElement:
    """Defines the query for a view."""

    def __init__(self):
        self.Where = WhereElement()
        self.OrderBy = OrderByElement()
        self.GroupBy = GroupByElement()

    @staticmethod
    def parse(expr):
        return QueryElement()

    def __repr__(self):
        return f"<Query>{str(self.Where)}</Query>"


class RowLimitElement(object):
    """Sets the row limit for the number of items to display in a view."""

    def __init__(self, top=None):
        """
        :param int top:
        """
        self.Top = top

    def __str__(self):
        return f'<RowLimit Paged="TRUE">{self.Top}</RowLimit>'


class ViewElement:
    """"""

    def __init__(
        self,
        scope=ViewScope.DefaultValue,
        query=QueryElement(),
        row_limit=RowLimitElement(),
    ):
        self.Scope = scope
        self.Query = query
        self.RowLimit = row_limit

    def __str__(self):
        return f'<View Scope="{self.Scope}"><Query>{str(self.Query)}</Query></View>'


class CamlQuery(ClientValue):
    def __init__(
        self,
        dates_in_utc: bool = True,
        view_xml: str = None,
        list_item_collection_position: ListItemCollectionPosition = None,
        folder_server_relative_url: str = None,
        allow_incremental_results: bool = True,
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
