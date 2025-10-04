from office365.runtime.client_value import ClientValue


class WebPartDetailsWrapper(ClientValue):

    def __init__(
        self, instance_id: str = None, is_internal: bool = None, manifest_id: str = None
    ):
        self.InstanceId = instance_id
        self.IsInternal = is_internal
        self.ManifestId = manifest_id
