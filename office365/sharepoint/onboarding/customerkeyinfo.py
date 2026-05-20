from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.onboarding.customerkeyvaultinfo import CustomerKeyVaultInfo


@dataclass
class CustomerKeyInfo(ClientValue):
    AvailabilityKeyVault: CustomerKeyVaultInfo = field(default_factory=CustomerKeyVaultInfo)
    PrimaryKeyVault: CustomerKeyVaultInfo = field(default_factory=CustomerKeyVaultInfo)
    SecondaryKeyVault: CustomerKeyVaultInfo = field(default_factory=CustomerKeyVaultInfo)
