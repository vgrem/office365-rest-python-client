from typing_extensions import Self

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.search.query.reordering_rule import ReorderingRule


class ReorderingRuleCollection(Entity):
    """Contains information about how to reorder the search results."""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Query.ReorderingRuleCollection"

    @property
    def items(self) -> ClientValueCollection[ReorderingRule]:
        """Gets the Items property"""
        return self.properties.get("Items", ClientValueCollection[ReorderingRule](ReorderingRule))

    def add(self, match_type: int, match_value: str, boost: int) -> Self:
        """Add operation.

        Args:
            match_type (int): matchType parameter
            match_value (str): matchValue parameter
            boost (int): boost parameter
        """
        qry = ServiceOperationQuery(
            self, "Add", None, {"matchType": match_type, "matchValue": match_value, "boost": boost}, None, None
        )
        self.context.add_query(qry)
        return self

    def clear(self) -> Self:
        """Clear operation."""
        qry = ServiceOperationQuery(self, "Clear", None, {}, None, None)
        self.context.add_query(qry)
        return self
