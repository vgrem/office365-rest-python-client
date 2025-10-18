from office365.runtime.client_value import ClientValue


class TaxonomyMetadata(ClientValue):
    """Represents taxonomy metadata for SharePoint publishing."""

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
        """Initializes a new instance of TaxonomyMetadata.

        Args:
            anchor_id: GUID representing the anchor term ID for taxonomy operations
            excluded_termset: If true, excludes specified term sets from operations
            exclude_keyword: If true, excludes keywords from taxonomy operations
            is_add_terms: If true, allows adding new terms during operations
            is_include_deprecated: If true, includes deprecated terms in results
            is_include_path_data: If true, includes path data for terms
            is_include_unavailable: If true, includes unavailable terms in results
            is_span_term_sets: If true, operations span across multiple term sets
            is_span_term_stores: If true, operations span across multiple term stores
            lcid: Locale ID for language-specific term operations (default: 1033)
            ssp_list: Comma-separated list of shared service provider IDs
            term_set_list: Comma-separated list of term set IDs
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
