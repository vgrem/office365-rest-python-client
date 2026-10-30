from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata
from office365.security.cases.exportfilestructure import ExportFileStructure
from office365.security.cases.exportoptions import ExportOptions
from office365.security.ediscovery.review_set import EdiscoveryReviewSet
from office365.security.ediscovery.review_set_query import (
    EdiscoveryReviewSetQuery,
)
from office365.security.export_file_metadata import ExportFileMetadata


class EdiscoveryExportOperation(PollableOperation, Entity):
    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="exportOptions")
    @property
    def export_options(self) -> ExportOptions:
        """Gets the exportOptions property"""
        return self.properties.get("exportOptions", ExportOptions.originalFiles)

    @odata(name="exportStructure")
    @property
    def export_structure(self) -> ExportFileStructure:
        """Gets the exportStructure property"""
        return self.properties.get("exportStructure", ExportFileStructure.none)

    @odata(name="outputName")
    @property
    def output_name(self) -> Optional[str]:
        """Gets the outputName property"""
        return self.properties.get("outputName", None)

    @odata(name="reviewSet", navigation=True)
    @property
    def review_set(self) -> EdiscoveryReviewSet:
        """Gets the reviewSet property"""
        return self.properties.get(
            "reviewSet", EdiscoveryReviewSet(self.context, ResourcePath("reviewSet", self.resource_path))
        )

    @odata(name="reviewSetQuery", navigation=True)
    @property
    def review_set_query(self) -> EdiscoveryReviewSetQuery:
        """Gets the reviewSetQuery property"""
        return self.properties.get(
            "reviewSetQuery", EdiscoveryReviewSetQuery(self.context, ResourcePath("reviewSetQuery", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoveryExportOperation"

    @odata(name="exportFileMetadata")
    @property
    def export_file_metadata(self) -> ClientValueCollection[ExportFileMetadata]:
        """Gets the exportFileMetadata property"""
        return self.properties.get("exportFileMetadata", ClientValueCollection[ExportFileMetadata](ExportFileMetadata))
