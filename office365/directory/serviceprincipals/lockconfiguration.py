from typing import Optional

from office365.runtime.client_value import ClientValue


class ServicePrincipalLockConfiguration(ClientValue):
    def __init__(
        self,
        all_properties: Optional[bool] = None,
        credentials_with_usage_sign: Optional[bool] = None,
        credentials_with_usage_verify: Optional[bool] = None,
        is_enabled: Optional[bool] = None,
        token_encryption_key_id: Optional[bool] = None,
    ):
        self.allProperties = all_properties
        self.credentialsWithUsageSign = credentials_with_usage_sign
        self.credentialsWithUsageVerify = credentials_with_usage_verify
        self.isEnabled = is_enabled
        self.tokenEncryptionKeyId = token_encryption_key_id

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServicePrincipalLockConfiguration"
