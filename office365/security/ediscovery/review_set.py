from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb
from office365.security.ediscovery.review_set_query import EdiscoveryReviewSetQuery

if TYPE_CHECKING:
    from office365.security.cases.additionaldataoptions import AdditionalDataOptions
    from office365.security.cases.exportfilestructure import ExportFileStructure
    from office365.security.cases.exportoptions import ExportOptions
    from office365.security.cases.itemstoinclude import ItemsToInclude
    from office365.security.cloudattachmentversion import CloudAttachmentVersion
    from office365.security.ediscovery.search import EdiscoverySearch
    from office365.security.search.documentversion import DocumentVersion


class EdiscoveryReviewSet(Entity):
    @odata(name="queries", navigation=True)
    @property
    def queries(self) -> EntityCollection[EdiscoveryReviewSetQuery]:
        """Gets the queries property"""
        return self.properties.get(
            "queries",
            EntityCollection[EdiscoveryReviewSetQuery](
                self.context, EdiscoveryReviewSetQuery, ResourcePath("queries", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoveryReviewSet"

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["eDiscovery.Read.All", "eDiscovery.ReadWrite.All"],
        application=["eDiscovery.Read.All", "eDiscovery.ReadWrite.All"],
    )
    def add_to_review_set(
        self,
        search: EdiscoverySearch,
        additional_data_options: AdditionalDataOptions,
        items_to_include: ItemsToInclude,
        cloud_attachment_version: CloudAttachmentVersion,
        document_version: DocumentVersion,
    ) -> Self:
        """addToReviewSet operation.

        Args:
            search (EdiscoverySearch):
                search parameter
            additional_data_options (AdditionalDataOptions):
                additionalDataOptions parameter
            items_to_include (ItemsToInclude):
                itemsToInclude parameter
            cloud_attachment_version (CloudAttachmentVersion):
                cloudAttachmentVersion parameter
            document_version (DocumentVersion):
                documentVersion parameter
        """
        qry = ServiceOperationQuery(
            self,
            "addToReviewSet",
            None,
            {
                "search": search,
                "additionalDataOptions": additional_data_options,
                "itemsToInclude": items_to_include,
                "cloudAttachmentVersion": cloud_attachment_version,
                "documentVersion": document_version,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["eDiscovery.Read.All", "eDiscovery.ReadWrite.All"],
        application=["eDiscovery.Read.All", "eDiscovery.ReadWrite.All"],
    )
    def export(
        self, output_name: str, description: str, export_options: ExportOptions, export_structure: ExportFileStructure
    ) -> Self:
        """export operation.

        Args:
            output_name (str):
                outputName parameter
            description (str):
                description parameter
            export_options (ExportOptions):
                exportOptions parameter
            export_structure (ExportFileStructure):
                exportStructure parameter
        """
        qry = ServiceOperationQuery(
            self,
            "export",
            None,
            {
                "outputName": output_name,
                "description": description,
                "exportOptions": export_options,
                "exportStructure": export_structure,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self
