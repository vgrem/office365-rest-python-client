from __future__ import annotations

from dataclasses import field

from office365.directory.applications.data_retention_level import DataRetentionLevel
from office365.directory.applications.riskfactors.legal_info_gdpr import ApplicationRiskFactorLegalInfoGdpr
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ApplicationRiskFactorLegalInfo(ClientValue):
    dataRetention: DataRetentionLevel = DataRetentionLevel.none
    hasDataOwnership: bool | None = None
    hasDmca: bool | None = None
    gdpr: ApplicationRiskFactorLegalInfoGdpr = field(default_factory=ApplicationRiskFactorLegalInfoGdpr)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationRiskFactorLegalInfo"
