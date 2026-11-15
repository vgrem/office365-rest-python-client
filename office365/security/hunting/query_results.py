from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.filters.single_property_schema import SinglePropertySchema
from office365.security.hunting.row_result import HuntingRowResult


class HuntingQueryResults(ClientValue):
    """The results of running a query for advanced hunting."""

    results: ClientValueCollection[HuntingRowResult] = field(
        default_factory=lambda: ClientValueCollection(HuntingRowResult)
    )
    schema: ClientValueCollection[SinglePropertySchema] = field(
        default_factory=lambda: ClientValueCollection(SinglePropertySchema)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.HuntingQueryResults"
