from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata
from office365.security.cases.additionaldataoptions import (
    AdditionalDataOptions,
)
from office365.security.cases.itemstoinclude import ItemsToInclude
from office365.security.cloudattachmentversion import CloudAttachmentVersion
from office365.security.ediscovery.review_set import EdiscoveryReviewSet
from office365.security.report_file_metadata import ReportFileMetadata
from office365.security.search.documentversion import DocumentVersion

if TYPE_CHECKING:
    from office365.security.ediscovery.search import EdiscoverySearch


class EdiscoveryAddToReviewSetOperation(PollableOperation, Entity):
    @odata(name="additionalDataOptions")
    @property
    def additional_data_options(self) -> AdditionalDataOptions:
        """Gets the additionalDataOptions property"""
        return self.properties.get("additionalDataOptions", AdditionalDataOptions.allVersions)

    @odata(name="cloudAttachmentVersion")
    @property
    def cloud_attachment_version(self) -> CloudAttachmentVersion:
        """Gets the cloudAttachmentVersion property"""
        return self.properties.get("cloudAttachmentVersion", CloudAttachmentVersion.latest)

    @odata(name="documentVersion")
    @property
    def document_version(self) -> DocumentVersion:
        """Gets the documentVersion property"""
        return self.properties.get("documentVersion", DocumentVersion.latest)

    @odata(name="itemsToInclude")
    @property
    def items_to_include(self) -> ItemsToInclude:
        """Gets the itemsToInclude property"""
        return self.properties.get("itemsToInclude", ItemsToInclude.searchHits)

    @odata(name="reviewSet", navigation=True)
    @property
    def review_set(self) -> EdiscoveryReviewSet:
        """Gets the reviewSet property"""
        return self.properties.get(
            "reviewSet", EdiscoveryReviewSet(self.context, ResourcePath("reviewSet", self.resource_path))
        )

    @odata(name="search", navigation=True)
    @property
    def search(self) -> EdiscoverySearch:
        """Gets the search property"""
        return self.properties.get("search", EdiscoverySearch(self.context, ResourcePath("search", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoveryAddToReviewSetOperation"

    @odata(name="reportFileMetadata")
    @property
    def report_file_metadata(self) -> ClientValueCollection[ReportFileMetadata]:
        """Gets the reportFileMetadata property"""
        return self.properties.get("reportFileMetadata", ClientValueCollection[ReportFileMetadata](ReportFileMetadata))
