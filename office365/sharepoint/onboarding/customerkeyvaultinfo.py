from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CustomerKeyVaultInfo(ClientValue):
    KeyName: Optional[str] = None
    KeyVersion: Optional[str] = None
    ResourceGroupName: Optional[str] = None
    SubscriptionId: Optional[str] = None
    Uri: Optional[str] = None
    VaultName: Optional[str] = None
