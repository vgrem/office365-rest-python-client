from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class TaxonomyMetadata(ClientValue):
    """Represents taxonomy metadata for SharePoint publishing.

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

    anchorId: Optional[str] = None
    excludedTermset: Optional[bool] = None
    excludeKeyword: Optional[bool] = None
    isAddTerms: Optional[bool] = None
    isIncludeDeprecated: Optional[bool] = None
    isIncludePathData: Optional[bool] = None
    isIncludeUnavailable: Optional[bool] = None
    isSpanTermSets: Optional[bool] = None
    isSpanTermStores: Optional[bool] = None
    lcid: Optional[int] = None
    sspList: Optional[str] = None
    termSetList: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.TaxonomyMetadata"
