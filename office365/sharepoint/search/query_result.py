from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.custom_result import CustomResult
from office365.sharepoint.search.refinement_results import RefinementResults
from office365.sharepoint.search.relevant_results import RelevantResults
from office365.sharepoint.search.special_term_results import SpecialTermResults


@dataclass
class QueryResult(ClientValue):
    """
    The QueryResult type is a grouping of result tables, where each contained result table is a ResultTable
    as specified in [MS-QSSWS] section 3.1.4.1.3.6.
    """

    QueryId: str | None = None
    QueryRuleId: str | None = None
    RefinementResults: RefinementResults = field(default_factory=RefinementResults)
    CustomResults: ClientValueCollection[CustomResult] = field(
        default_factory=lambda: ClientValueCollection(CustomResult)
    )
    RelevantResults: RelevantResults = field(default_factory=RelevantResults)
    SpecialTermResults: SpecialTermResults = field(default_factory=SpecialTermResults)

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.QueryResult"
