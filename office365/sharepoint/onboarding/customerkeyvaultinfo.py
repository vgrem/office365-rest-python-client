from typing import Optional

from office365.runtime.client_value import ClientValue


class CustomerKeyVaultInfo(ClientValue):
    def __init__(
        self,
        key_vault_name: Optional[str] = None,
        key_vault_resource_group_name: Optional[str] = None,
        key_vault_subscription_id: Optional[str] = None,
        key_vault_url: Optional[str] = None,
        key_vault_resource_name: Optional[str] = None,
        key_vault_resource_group_location: Optional[str] = None,
    ):
        self.KeyName = key_name
        self.KeyVersion = key_version
        self.ResourceGroupName = resource_group_name
        self.SubscriptionId = subscription_id
        self.Uri = uri
        self.VaultName = vault_name
