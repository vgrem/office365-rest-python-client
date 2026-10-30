from __future__ import annotations

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.pollable import PollableOperation
from office365.runtime.types.odata_property import odata
from office365.security.report_file_metadata import ReportFileMetadata


class EdiscoveryHoldPolicySyncOperation(PollableOperation, Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoveryHoldPolicySyncOperation"

    @odata(name="reportFileMetadata")
    @property
    def report_file_metadata(self) -> ClientValueCollection[ReportFileMetadata]:
        """Gets the reportFileMetadata property"""
        return self.properties.get("reportFileMetadata", ClientValueCollection[ReportFileMetadata](ReportFileMetadata))
