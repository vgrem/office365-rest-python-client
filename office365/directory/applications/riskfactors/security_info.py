from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.applications.password_policy import PasswordPolicy
from office365.directory.applications.rest_encryption_type import RestEncryptionType
from office365.directory.applications.riskfactors.certificate_info import ApplicationRiskFactorCertificateInfo
from office365.directory.applications.ssl_version import SslVersion
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ApplicationRiskFactorSecurityInfo(ClientValue):
    certificate: ApplicationRiskFactorCertificateInfo = field(default_factory=ApplicationRiskFactorCertificateInfo)
    domainToCheck: str | None = None
    hasAdminAuditTrail: bool | None = None
    hasAnonymousUsage: bool | None = None
    hasDataAuditTrail: bool | None = None
    hasDataClassification: bool | None = None
    hasDataEncrypted: bool | None = None
    hasEnforceTransportEnc: bool | None = None
    hasIpRestriction: bool | None = None
    hasMFA: bool | None = None
    hasPenTest: bool | None = None
    hasRememberPassword: bool | None = None
    hasSamlSupport: bool | None = None
    hasUserAuditLogs: bool | None = None
    hasUserDataUpload: bool | None = None
    hasUserRolesSupport: bool | None = None
    hasValidCertName: bool | None = None
    httpsSecurityHeaders: StringCollection = field(default_factory=StringCollection)
    isCertTrusted: bool | None = None
    isDrownVulnerable: bool | None = None
    isHeartbleedProof: bool | None = None
    latestValidSSL: SslVersion = SslVersion.none
    passwordPolicy: PasswordPolicy = PasswordPolicy.none
    restEncryptionType: RestEncryptionType = RestEncryptionType.none

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationRiskFactorSecurityInfo"
