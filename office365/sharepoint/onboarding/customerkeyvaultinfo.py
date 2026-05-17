from typing import Optional

from office365.runtime.client_value import ClientValue


class CustomerKeyVaultInfo(ClientValue):
    def __init__(
        self,
        key_name: Optional[str] = None,
        key_version: Optional[str] = None,
        resource_group_name: Optional[str] = None,
        subscription_id: Optional[str] = None,
        uri: Optional[str] = None,
        vault_name: Optional[str] = None,
    ):
        self.KeyName = key_name
        self.KeyVersion = key_version
        self.ResourceGroupName = resource_group_name
        self.SubscriptionId = subscription_id
        self.Uri = uri
        self.VaultName = vault_name
