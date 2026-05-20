from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CustomerKeyStatusInfo(ClientValue):
    availability_key_vault_uri: Optional[str] = None
    primary_key_vault: Optional[str] = None
    primary_key_vault_uri: Optional[str] = None
    recovery_enabled: Optional[bool] = None
    registration_progress: Optional[str] = None
    secondary_key_vault_uri: Optional[str] = None
    status: Optional[int] = None
    tenant_has_key: Optional[bool] = None
    tenant_key_version: Optional[str] = None
    tenant_key_vault: Optional[str] = None
    tenant_key_vault_uri: Optional[str] = None
