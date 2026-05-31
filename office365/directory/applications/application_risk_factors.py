from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.applications.riskfactors.general_info import ApplicationRiskFactorGeneralInfo
from office365.directory.applications.riskfactors.legal_info import ApplicationRiskFactorLegalInfo
from office365.directory.applications.riskfactors.security_info import ApplicationRiskFactorSecurityInfo
from office365.directory.applications.security_compliance import ApplicationSecurityCompliance
from office365.runtime.client_value import ClientValue


@dataclass
class ApplicationRiskFactors(ClientValue):
    compliance: ApplicationSecurityCompliance = field(default_factory=ApplicationSecurityCompliance)
    general: ApplicationRiskFactorGeneralInfo = field(default_factory=ApplicationRiskFactorGeneralInfo)
    legal: ApplicationRiskFactorLegalInfo = field(default_factory=ApplicationRiskFactorLegalInfo)
    security: ApplicationRiskFactorSecurityInfo = field(default_factory=ApplicationRiskFactorSecurityInfo)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationRiskFactors"
