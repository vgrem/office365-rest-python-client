from office365.runtime.client_value import ClientValue


class ServicePrincipalLockConfiguration(ClientValue):
    def __init__(
        self,
        all_properties: bool = None,
        credentials_with_usage_sign: bool = None,
        credentials_with_usage_verify: bool = None,
        is_enabled: bool = None,
        token_encryption_key_id: bool = None,
    ):
        self.allProperties = all_properties
        self.credentialsWithUsageSign = credentials_with_usage_sign
        self.credentialsWithUsageVerify = credentials_with_usage_verify
        self.isEnabled = is_enabled
        self.tokenEncryptionKeyId = token_encryption_key_id

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServicePrincipalLockConfiguration"
