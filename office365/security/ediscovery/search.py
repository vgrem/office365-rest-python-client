from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.security.ediscovery.noncustodial_data_source import (
    EdiscoveryNoncustodialDataSource,
)
from office365.security.ediscovery.operations.add_to_review_set import (
    EdiscoveryAddToReviewSetOperation,
)
from office365.security.search.data_source import DataSource
from office365.security.search.datasourcescopes import DataSourceScopes

if TYPE_CHECKING:
    from office365.security.cases.additionaloptions import AdditionalOptions
    from office365.security.cases.exportcriteria import ExportCriteria
    from office365.security.cases.exportformat import ExportFormat
    from office365.security.cases.exportlocation import ExportLocation
    from office365.security.cases.statisticsoptions import StatisticsOptions
    from office365.security.cloudattachmentversion import CloudAttachmentVersion
    from office365.security.ediscovery.ediscovery_estimate_operation import (
        EdiscoveryEstimateOperation,
    )
    from office365.security.purgeareas import PurgeAreas
    from office365.security.purgetype import PurgeType
    from office365.security.search.documentversion import DocumentVersion


class EdiscoverySearch(Entity):
    @odata(name="dataSourceScopes")
    @property
    def data_source_scopes(self) -> DataSourceScopes:
        """Gets the dataSourceScopes property"""
        return self.properties.get("dataSourceScopes", DataSourceScopes.none)

    @odata(name="additionalSources", navigation=True)
    @property
    def additional_sources(self) -> EntityCollection[DataSource]:
        """Gets the additionalSources property"""
        return self.properties.get(
            "additionalSources",
            EntityCollection[DataSource](
                self.context, DataSource, ResourcePath("additionalSources", self.resource_path)
            ),
        )

    @odata(name="addToReviewSetOperation", navigation=True)
    @property
    def add_to_review_set_operation(self) -> EdiscoveryAddToReviewSetOperation:
        """Gets the addToReviewSetOperation property"""
        return self.properties.get(
            "addToReviewSetOperation",
            EdiscoveryAddToReviewSetOperation(self.context, ResourcePath("addToReviewSetOperation", self.resource_path)),
        )

    @odata(name="custodianSources", navigation=True)
    @property
    def custodian_sources(self) -> EntityCollection[DataSource]:
        """Gets the custodianSources property"""
        return self.properties.get(
            "custodianSources",
            EntityCollection[DataSource](self.context, DataSource, ResourcePath("custodianSources", self.resource_path)),
        )

    @odata(name="noncustodialSources", navigation=True)
    @property
    def noncustodial_sources(self) -> EntityCollection[EdiscoveryNoncustodialDataSource]:
        """Gets the noncustodialSources property"""
        return self.properties.get(
            "noncustodialSources",
            EntityCollection[EdiscoveryNoncustodialDataSource](
                self.context, EdiscoveryNoncustodialDataSource, ResourcePath("noncustodialSources", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoverySearch"

    @odata(name="lastEstimateStatisticsOperation", navigation=True)
    @property
    def last_estimate_statistics_operation(self) -> EdiscoveryEstimateOperation:
        """Gets the lastEstimateStatisticsOperation property"""
        from office365.security.ediscovery.ediscovery_estimate_operation import (
            EdiscoveryEstimateOperation,
        )

        return self.properties.get(
            "lastEstimateStatisticsOperation",
            EdiscoveryEstimateOperation(
                self.context, ResourcePath("lastEstimateStatisticsOperation", self.resource_path)
            ),
        )

    def estimate_statistics(self, statistics_options: StatisticsOptions) -> Self:
        """estimateStatistics operation.

        Args:
            statistics_options (StatisticsOptions):
                statisticsOptions parameter
        """
        qry = ServiceOperationQuery(
            self, "estimateStatistics", None, {"statisticsOptions": statistics_options}, None, None
        )
        self.context.add_query(qry)
        return self

    def export_report(
        self,
        display_name: str,
        description: str,
        export_criteria: ExportCriteria,
        export_location: ExportLocation,
        additional_options: AdditionalOptions,
        cloud_attachment_version: CloudAttachmentVersion,
        document_version: DocumentVersion,
    ) -> Self:
        """exportReport operation.

        Args:
            display_name (str):
                displayName parameter
            description (str):
                description parameter
            export_criteria (ExportCriteria):
                exportCriteria parameter
            export_location (ExportLocation):
                exportLocation parameter
            additional_options (AdditionalOptions):
                additionalOptions parameter
            cloud_attachment_version (CloudAttachmentVersion):
                cloudAttachmentVersion parameter
            document_version (DocumentVersion):
                documentVersion parameter
        """
        qry = ServiceOperationQuery(
            self,
            "exportReport",
            None,
            {
                "displayName": display_name,
                "description": description,
                "exportCriteria": export_criteria,
                "exportLocation": export_location,
                "additionalOptions": additional_options,
                "cloudAttachmentVersion": cloud_attachment_version,
                "documentVersion": document_version,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def export_result(
        self,
        display_name: str,
        description: str,
        export_criteria: ExportCriteria,
        export_location: ExportLocation,
        additional_options: AdditionalOptions,
        export_format: ExportFormat,
        export_single_items: bool,
        cloud_attachment_version: CloudAttachmentVersion,
        document_version: DocumentVersion,
    ) -> Self:
        """exportResult operation.

        Args:
            display_name (str):
                displayName parameter
            description (str):
                description parameter
            export_criteria (ExportCriteria):
                exportCriteria parameter
            export_location (ExportLocation):
                exportLocation parameter
            additional_options (AdditionalOptions):
                additionalOptions parameter
            export_format (ExportFormat):
                exportFormat parameter
            export_single_items (bool):
                exportSingleItems parameter
            cloud_attachment_version (CloudAttachmentVersion):
                cloudAttachmentVersion parameter
            document_version (DocumentVersion):
                documentVersion parameter
        """
        qry = ServiceOperationQuery(
            self,
            "exportResult",
            None,
            {
                "displayName": display_name,
                "description": description,
                "exportCriteria": export_criteria,
                "exportLocation": export_location,
                "additionalOptions": additional_options,
                "exportFormat": export_format,
                "exportSingleItems": export_single_items,
                "cloudAttachmentVersion": cloud_attachment_version,
                "documentVersion": document_version,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def purge_data(self, purge_type: PurgeType, purge_areas: PurgeAreas) -> Self:
        """purgeData operation.

        Args:
            purge_type (PurgeType):
                purgeType parameter
            purge_areas (PurgeAreas):
                purgeAreas parameter
        """
        qry = ServiceOperationQuery(
            self, "purgeData", None, {"purgeType": purge_type, "purgeAreas": purge_areas}, None, None
        )
        self.context.add_query(qry)
        return self
