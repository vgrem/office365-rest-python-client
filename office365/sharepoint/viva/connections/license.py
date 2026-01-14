from office365.runtime.client_value import ClientValue


class VivaConnectionsLicense(ClientValue):
    def __init__(self, is_tenant_enabled: bool = None, is_user_enabled: bool = None):
        self.is_tenant_enabled = is_tenant_enabled
        self.is_user_enabled = is_user_enabled
