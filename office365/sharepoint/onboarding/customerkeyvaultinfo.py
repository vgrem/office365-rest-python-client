from office365.runtime.client_value import ClientValue


class CustomerKeyVaultInfo(ClientValue):

    def __init__(
        self,
        key_name: str = None,
        key_version: str = None,
        resource_group_name: str = None,
        subscription_id: str = None,
        uri: str = None,
        vault_name: str = None,
    ):
        self.KeyName = key_name
        self.KeyVersion = key_version
        self.ResourceGroupName = resource_group_name
        self.SubscriptionId = subscription_id
        self.Uri = uri
        self.VaultName = vault_name
