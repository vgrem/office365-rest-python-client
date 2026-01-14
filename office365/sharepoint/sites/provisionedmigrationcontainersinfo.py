from office365.runtime.client_value import ClientValue


class ProvisionedMigrationContainersInfo(ClientValue):
    def __init__(
        self,
        data_container_uri: str = None,
        encryption_key: bytes = None,
        metadata_container_uri: str = None,
    ):
        self.data_container_uri = data_container_uri
        self.encryption_key = encryption_key
        self.metadata_container_uri = metadata_container_uri
