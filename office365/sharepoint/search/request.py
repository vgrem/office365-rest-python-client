from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.search.query.property import QueryProperty
from office365.sharepoint.search.query.reordering_rule import ReorderingRule
from office365.sharepoint.search.query.sort.sort import Sort


@dataclass
class SearchRequest(ClientValue):
    """
    The SearchRequest structure defines the HTTP BODY of the HTTP POST postquery operation as specified
    in section 3.1.5.7.2.1.3. The postquery operation together with the SearchRequest structure is similar
    to the query operation as specified in section 3.1.5.7.2.1.4, and is provided as a means to overcome
    Uniform Resource Locator (URL) length limitations that some clients experience with HTTP GET operations.
    """

    Querytext: str | None = None
    SelectProperties: StringCollection = field(default_factory=StringCollection)
    ClientType: str | None = None
    CollapseSpecification: str | None = None
    Culture: str | None = None
    EnableSorting: bool | None = None
    SortList: ClientValueCollection[Sort] = field(default_factory=lambda: ClientValueCollection(Sort))
    TrimDuplicates: bool = False
    RankingModelId: str | None = None
    RowLimit: int | None = None
    RowsPerPage: int | None = None
    QueryTemplate: str | None = None
    SummaryLength: int | None = None
    StartRow: int | None = None
    EnableQueryRules: bool | None = None
    SourceId: str | None = None
    ReorderingRules: ClientValueCollection[ReorderingRule] = field(
        default_factory=lambda: ClientValueCollection(ReorderingRule)
    )
    Properties: ClientValueCollection[QueryProperty] = field(
        default_factory=lambda: ClientValueCollection(QueryProperty)
    )
    UILanguage: int | None = None
    HitHighlightedProperties: StringCollection = field(default_factory=StringCollection)
    HitHighlightedMultivaluePropertyLimit: int | None = None
    BlockDedupeMode: int | None = None
    BypassResultTypes: bool | None = None
    DesiredSnippetLength: int | None = None
    EnableFQL: bool | None = None
    EnableInterleaving: bool | None = None
    EnableNicknames: bool | None = None
    EnableOrderingHitHighlightedProperty: bool | None = None
    EnablePhonetic: bool | None = None
    EnableStemming: bool | None = None
    GenerateBlockRankLog: bool | None = None
    HiddenConstraints: str | None = None
    ImpressionId: str | None = None
    MaxSnippetLength: int | None = None
    OLSQuerySession: str | None = None
    PersonalizationData: str | None = None
    ProcessBestBets: bool | None = None
    ProcessPersonalFavorites: bool | None = None
    PropertiesToGenerateAcronyms: Optional[StringCollection] = None
    QueryTag: str | None = None
    QueryTemplatePropertiesUrl: str | None = None
    RefinementFilters: Optional[StringCollection] = None
    Refiners: str | None = None
    ResultsUrl: str | None = None
    Timeout: int | None = None
    TimeZoneId: int | None = None
    TotalRowsExactMinimum: int | None = None
    TrimDuplicatesIncludeId: int | None = None
    UseOLSQuery: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.SearchRequest"
