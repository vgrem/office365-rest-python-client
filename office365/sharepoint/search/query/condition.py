from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class QueryCondition(ClientValue):

    def __init__(
        self,
        lcid: int = None,
        matching_options: str = None,
        query_condition_type: str = None,
        subject_terms_origin: str = None,
        terms: StringCollection = StringCollection(),
    ):
        """This object contains the conditions for the promoted result"""
        self.LCID = lcid
        self.MatchingOptions = matching_options
        self.QueryConditionType = query_condition_type
        self.SubjectTermsOrigin = subject_terms_origin
        self.Terms = terms

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.QueryCondition"
