from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.onboarding.customerkeyvaultinfo import CustomerKeyVaultInfo


@value
class CustomerKeyInfo(ClientValue):
    AvailabilityKeyVault: CustomerKeyVaultInfo = field(default_factory=CustomerKeyVaultInfo)
    PrimaryKeyVault: CustomerKeyVaultInfo = field(default_factory=CustomerKeyVaultInfo)
    SecondaryKeyVault: CustomerKeyVaultInfo = field(default_factory=CustomerKeyVaultInfo)
