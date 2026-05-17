from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.context_condition import ContextCondition
from office365.sharepoint.search.promotedresults import PromotedResults
from office365.sharepoint.search.query.condition import QueryCondition


class PromotedResultQueryRule(ClientValue):
    """
    This object contains properties that describe one promoted result for the tenant/Search
    Service Application or site collection.
    """

    def __init__(
        self,
        contact=None,
        context_conditions=None,
        creation_date=None,
        display_name: Optional[str] = None,
        end_date: Optional[datetime] = None,
        is_promoted_results_only: Optional[bool] = None,
        last_modified_date: Optional[datetime] = None,
        promoted_results: Optional[ClientValueCollection[PromotedResults]] = None,
        query_conditions: Optional[ClientValueCollection[QueryCondition]] = None,
        review_date: Optional[datetime] = None,
        start_date: Optional[datetime] = None,
    ):
        """
        :param str contact: This property contains the contact information for the promoted result.
        :param list[ContextCondition] context_conditions: This property contains the context condition for the promoted
            result.
        :param str creation_date: This property is the creation date for the promoted result.
        """
        self.Contact = contact
        self.ContextConditions = ClientValueCollection(ContextCondition, context_conditions)
        self.CreationDate = creation_date
        self.DisplayName = display_name
        self.EndDate = end_date
        self.IsPromotedResultsOnly = is_promoted_results_only
        self.LastModifiedDate = last_modified_date
        self.PromotedResults = promoted_results
        self.QueryConditions = query_conditions
        self.ReviewDate = review_date
        self.StartDate = start_date

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.PromotedResultQueryRule"
