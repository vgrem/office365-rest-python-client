from office365.runtime.client_value import ClientValue


class ReportQueryRulesData(ClientValue):

    def __init__(
        self,
        dictionary_terms: str = None,
        owner_type: str = None,
        percentage_promoted_result: str = None,
        promoted_result_clicks: str = None,
        promoted_result_id: str = None,
        promoted_result_url: str = None,
        promoted_result_url_name: str = None,
        query_rule: str = None,
        query_rule_id: str = None,
        result_source: str = None,
        times_fired: str = None,
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
