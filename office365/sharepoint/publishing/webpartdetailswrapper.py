from typing import Optional

from office365.runtime.client_value import ClientValue


class WebPartDetailsWrapper(ClientValue):
    def __init__(
        self, instance_id: Optional[str] = None, is_internal: Optional[bool] = None, manifest_id: Optional[str] = None
    ):
        self.InstanceId = instance_id
        self.IsInternal = is_internal
        self.ManifestId = manifest_id

    @property
    def entity_type_name(self):
        return "SP.Publishing.WebPartDetailsWrapper"
