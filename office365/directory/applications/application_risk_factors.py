from __future__ import annotations

from dataclasses import dataclass

from office365.directory.applications.riskfactors.general_info import ApplicationRiskFactorGeneralInfo
from office365.directory.applications.riskfactors.legal_info import ApplicationRiskFactorLegalInfo
from office365.directory.applications.security_compliance import ApplicationSecurityCompliance
from office365.runtime.client_value import ClientValue


@dataclass
class ApplicationRiskFactors(ClientValue):
    compliance: ApplicationSecurityCompliance = ApplicationSecurityCompliance()
    general: ApplicationRiskFactorGeneralInfo = ApplicationRiskFactorGeneralInfo()
    legal: ApplicationRiskFactorLegalInfo = ApplicationRiskFactorLegalInfo()

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationRiskFactors"
