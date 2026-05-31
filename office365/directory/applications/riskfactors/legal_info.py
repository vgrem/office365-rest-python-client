from __future__ import annotations
from dataclasses import dataclass
from office365.directory.applications.data_retention_level import DataRetentionLevel
from office365.runtime.client_value import ClientValue
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class ApplicationRiskFactorLegalInfo(ClientValue):
    dataRetention: DataRetentionLevel = DataRetentionLevel.none
    hasDataOwnership: bool | None = None
    hasDmca: bool | None = None
    gdpr: ApplicationRiskFactorLegalInfoGdpr = field(default_factory=ApplicationRiskFactorLegalInfoGdpr)

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.ApplicationRiskFactorLegalInfo'