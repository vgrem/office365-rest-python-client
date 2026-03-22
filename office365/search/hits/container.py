from __future__ import annotations

from typing import List

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.search.aggregation import SearchAggregation
from office365.search.hits.hit import SearchHit


class SearchHitsContainer(ClientValue):
    def __init__(
        self,
        hits: List[SearchHit] | None = None,
        more_results_available: bool | None = None,
        total: int | None = None,
        aggregations: List[SearchAggregation] | None = None,
    ):
        """
        Represent the list of search results.

        :param list[SearchHit] hits: A collection of the search results.
        :param int total: The total number of results. Note this is not the number of results on the page,
             but the total number of results satisfying the query.
        :param bool more_results_available: Provides information if more results are available.
            Based on this information, you can adjust the from and size properties of the searchRequest accordingly.
        :param list[SearchAggregation] aggregations:
        """
        super().__init__()
        self.hits = ClientValueCollection(SearchHit, hits)
        self.moreResultsAvailable = more_results_available
        self.total = total
        self.aggregations = ClientValueCollection(SearchAggregation, aggregations)
