from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata
from office365.security.cases.statisticsoptions import StatisticsOptions
from office365.security.ediscovery.search import EdiscoverySearch

if TYPE_CHECKING:
    from office365.security.report_file_metadata import ReportFileMetadata


class EdiscoveryEstimateOperation(PollableOperation, Entity):
    @odata(name="indexedItemCount")
    @property
    def indexed_item_count(self) -> Optional[int]:
        """Gets the indexedItemCount property"""
        return self.properties.get("indexedItemCount", None)

    @odata(name="indexedItemsSize")
    @property
    def indexed_items_size(self) -> Optional[int]:
        """Gets the indexedItemsSize property"""
        return self.properties.get("indexedItemsSize", None)

    @odata(name="mailboxCount")
    @property
    def mailbox_count(self) -> Optional[int]:
        """Gets the mailboxCount property"""
        return self.properties.get("mailboxCount", None)

    @odata(name="siteCount")
    @property
    def site_count(self) -> Optional[int]:
        """Gets the siteCount property"""
        return self.properties.get("siteCount", None)

    @odata(name="statisticsOptions")
    @property
    def statistics_options(self) -> StatisticsOptions:
        """Gets the statisticsOptions property"""
        return self.properties.get("statisticsOptions", StatisticsOptions.includeRefiners)

    @odata(name="unindexedItemCount")
    @property
    def unindexed_item_count(self) -> Optional[int]:
        """Gets the unindexedItemCount property"""
        return self.properties.get("unindexedItemCount", None)

    @odata(name="unindexedItemsSize")
    @property
    def unindexed_items_size(self) -> Optional[int]:
        """Gets the unindexedItemsSize property"""
        return self.properties.get("unindexedItemsSize", None)

    @odata(name="search", navigation=True)
    @property
    def search(self) -> EdiscoverySearch:
        """Gets the search property"""
        return self.properties.get("search", EdiscoverySearch(self.context, ResourcePath("search", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoveryEstimateOperation"

    @odata(name="reportFileMetadata")
    @property
    def report_file_metadata(self) -> ClientValueCollection[ReportFileMetadata]:
        """Gets the reportFileMetadata property"""
        from office365.security.report_file_metadata import ReportFileMetadata

        return self.properties.get("reportFileMetadata", ClientValueCollection[ReportFileMetadata](ReportFileMetadata))
