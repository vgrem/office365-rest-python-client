from uuid import UUID

from office365.runtime.client_value import ClientValue


class ResourceSpecificPermission(ClientValue):

    def __init__(
        self,
        description: str = None,
        display_name: str = None,
        id_: UUID = None,
        is_enabled: bool = None,
        value: str = None,
    ):
        self.description = description
        self.displayName = display_name
        self.id = id_
        self.isEnabled = is_enabled
        self.value = value

    @property
    def entity_type_name(self):
        return "microsoft.graph.ResourceSpecificPermission"
