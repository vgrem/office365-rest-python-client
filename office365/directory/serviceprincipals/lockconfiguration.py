from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ServicePrincipalLockConfiguration(ClientValue):
    allProperties: bool | None = None
    credentialsWithUsageSign: bool | None = None
    credentialsWithUsageVerify: bool | None = None
    isEnabled: bool | None = None
    tokenEncryptionKeyId: bool | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServicePrincipalLockConfiguration"
