from __future__ import annotations

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


class RowLimitElement:
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
