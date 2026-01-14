from office365.runtime.client_value import ClientValue
from office365.sharepoint.onboarding.customerkeyvaultinfo import CustomerKeyVaultInfo


class CustomerKeyInfo(ClientValue):
    def __init__(
        self,
        availability_key_vault: CustomerKeyVaultInfo = CustomerKeyVaultInfo(),
        primary_key_vault: CustomerKeyVaultInfo = CustomerKeyVaultInfo(),
        secondary_key_vault: CustomerKeyVaultInfo = CustomerKeyVaultInfo(),
    ):
        self.AvailabilityKeyVault = availability_key_vault
        self.PrimaryKeyVault = primary_key_vault
        self.SecondaryKeyVault = secondary_key_vault
