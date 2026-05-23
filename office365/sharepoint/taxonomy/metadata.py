from __future__ import annotations

from dataclasses import dataclass

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

    anchorId: str | None = None
    excludedTermset: bool | None = None
    excludeKeyword: bool | None = None
    isAddTerms: bool | None = None
    isIncludeDeprecated: bool | None = None
    isIncludePathData: bool | None = None
    isIncludeUnavailable: bool | None = None
    isSpanTermSets: bool | None = None
    isSpanTermStores: bool | None = None
    lcid: int | None = None
    sspList: str | None = None
    termSetList: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.TaxonomyMetadata"
