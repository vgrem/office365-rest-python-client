from __future__ import annotations

from typing import Optional

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.contentcenter.machinelearning.publicationresult import SPMachineLearningPublicationResult
from office365.sharepoint.entity import Entity


class SPMachineLearningPublicationsResult(Entity):
    @odata(name="Details", beta=True)
    @property
    def details(self) -> ClientValueCollection[SPMachineLearningPublicationResult]:
        """Gets the Details property"""
        return self.properties.get(
            "Details", ClientValueCollection[SPMachineLearningPublicationResult](SPMachineLearningPublicationResult)
        )

    @odata(name="TotalFailures", beta=True)
    @property
    def total_failures(self) -> Optional[int]:
        """Gets the TotalFailures property"""
        return self.properties.get("TotalFailures", None)

    @odata(name="TotalSuccesses", beta=True)
    @property
    def total_successes(self) -> Optional[int]:
        """Gets the TotalSuccesses property"""
        return self.properties.get("TotalSuccesses", None)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningPublicationsResult"
