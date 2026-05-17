from typing import Optional

from office365.runtime.client_value import ClientValue


class ReportQueryRulesData(ClientValue):
    def __init__(
        self,
        dictionary_terms: Optional[str] = None,
        owner_type: Optional[str] = None,
        percentage_promoted_result: Optional[str] = None,
        promoted_result_clicks: Optional[str] = None,
        promoted_result_id: Optional[str] = None,
        promoted_result_url: Optional[str] = None,
        promoted_result_url_name: Optional[str] = None,
        query_rule: Optional[str] = None,
        query_rule_id: Optional[str] = None,
        result_source: Optional[str] = None,
        times_fired: Optional[str] = None,
    ):
        self.DictionaryTerms = dictionary_terms
        self.OwnerType = owner_type
        self.PercentagePromotedResult = percentage_promoted_result
        self.PromotedResultClicks = promoted_result_clicks
        self.PromotedResultId = promoted_result_id
        self.PromotedResultURL = promoted_result_url
        self.PromotedResultURLName = promoted_result_url_name
        self.QueryRule = query_rule
        self.QueryRuleId = query_rule_id
        self.ResultSource = result_source
        self.TimesFired = times_fired

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ReportQueryRulesData"
