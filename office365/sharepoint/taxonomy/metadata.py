from office365.runtime.client_value import ClientValue


class TaxonomyMetadata(ClientValue):
    """ """

    def __init__(
        self,
        anchor_id: str = None,
        excluded_termset: bool = None,
        exclude_keyword: bool = None,
        is_add_terms: bool = None,
        is_include_deprecated: bool = None,
        is_include_path_data: bool = None,
        is_include_unavailable: bool = None,
        is_span_term_sets: bool = None,
        is_span_term_stores: bool = None,
        lcid: int = None,
        ssp_list: str = None,
        term_set_list: str = None,
    ):
        """
        :param str anchor_id:
        """
        self.anchorId = anchor_id
        self.excludedTermset = excluded_termset
        self.excludeKeyword = exclude_keyword
        self.isAddTerms = is_add_terms
        self.isIncludeDeprecated = is_include_deprecated
        self.isIncludePathData = is_include_path_data
        self.isIncludeUnavailable = is_include_unavailable
        self.isSpanTermSets = is_span_term_sets
        self.isSpanTermStores = is_span_term_stores
        self.lcid = lcid
        self.sspList = ssp_list
        self.termSetList = term_set_list

    @property
    def entity_type_name(self):
        return "SP.Publishing.TaxonomyMetadata"
