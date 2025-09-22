from office365.runtime.client_value import ClientValue


class CustomerKeyVaultInfo(ClientValue):
    pass


class CustomerKeyInfo(ClientValue):

    def __init__(
        self,
        availability_key_vault: CustomerKeyVaultInfo = None,
        primary_key_vault: CustomerKeyVaultInfo = None,
        secondary_key_vault: CustomerKeyVaultInfo = None,
    ):
        self.availability_key_vault = availability_key_vault
        self.primary_key_vault = primary_key_vault
        self.secondary_key_vault = secondary_key_vault
