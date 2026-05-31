from __future__ import annotations

from dataclasses import dataclass

from office365.directory.applications.data_retention_level import DataRetentionLevel
from office365.runtime.client_value import ClientValue


@dataclass
class ApplicationRiskFactorLegalInfo(ClientValue):
    dataRetention: DataRetentionLevel = DataRetentionLevel.none
    hasDataOwnership: bool | None = None
    hasDmca: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationRiskFactorLegalInfo"
