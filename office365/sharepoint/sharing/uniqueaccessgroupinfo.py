from uuid import UUID

from office365.runtime.client_value import ClientValue


class UniqueAccessGroupInfo(ClientValue):
    def __init__(self, enabled: bool = None, group_id: UUID = None):
        self.enabled = enabled
        self.groupId = group_id

    @property
    def entity_type_name(self):
        return "SP.Sharing.UniqueAccessGroupInfo"
