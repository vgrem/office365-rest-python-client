from typing import Optional

from office365.runtime.client_value import ClientValue


class CustomerKeyStatusInfo(ClientValue):
    def __init__(
        self,
        availability_key_vault_uri: Optional[str] = None,
        primary_key_vault: Optional[str] = None,
        primary_key_vault_uri: Optional[str] = None,
        recovery_enabled: Optional[bool] = None,
        registration_progress: Optional[str] = None,
        secondary_key_vault_uri: Optional[str] = None,
        status: Optional[int] = None,
        tenant_has_key: Optional[bool] = None,
        tenant_key_version: Optional[str] = None,
        tenant_key_vault: Optional[str] = None,
        tenant_key_vault_uri: Optional[str] = None,
    ):
        self.availability_key_vault_uri = availability_key_vault_uri
        self.primary_key_vault = primary_key_vault
        self.primary_key_vault_uri = primary_key_vault_uri
        self.recovery_enabled = recovery_enabled
        self.registration_progress = registration_progress
        self.secondary_key_vault_uri = secondary_key_vault_uri
        self.status = status
        self.tenant_has_key = tenant_has_key
        self.tenant_key_version = tenant_key_version
        self.tenant_key_vault = tenant_key_vault
        self.tenant_key_vault_uri = tenant_key_vault_uri
