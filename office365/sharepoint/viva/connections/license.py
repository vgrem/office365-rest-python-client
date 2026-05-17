from office365.runtime.client_value import ClientValue
from typing import Optional


class VivaConnectionsLicense(ClientValue):
    def __init__(self, is_tenant_enabled: Optional[bool] = None, is_user_enabled: Optional[bool] = None):
        self.is_tenant_enabled = is_tenant_enabled
        self.is_user_enabled = is_user_enabled
