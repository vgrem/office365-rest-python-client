from office365.runtime.client_value import ClientValue


class CustomerKeyStatusInfo(ClientValue):
    def __init__(
        self,
        availability_key_vault_uri: str = None,
        primary_key_vault_uri: str = None,
        recovery_enabled: bool = None,
        registration_progress: float = None,
        secondary_key_vault_uri: str = None,
        status: int = None,
    ):
        self.availability_key_vault_uri = availability_key_vault_uri
        self.primary_key_vault_uri = primary_key_vault_uri
        self.recovery_enabled = recovery_enabled
        self.registration_progress = registration_progress
        self.secondary_key_vault_uri = secondary_key_vault_uri
        self.status = status
