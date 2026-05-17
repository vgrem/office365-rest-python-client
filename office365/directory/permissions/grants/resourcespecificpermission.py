from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


class ResourceSpecificPermission(ClientValue):
    def __init__(
        self,
        description: Optional[str] = None,
        display_name: Optional[str] = None,
        id_: Optional[UUID] = None,
        is_enabled: Optional[bool] = None,
        value: Optional[str] = None,
    ):
        self.description = description
        self.displayName = display_name
        self.id = id_
        self.isEnabled = is_enabled
        self.value = value

    @property
    def entity_type_name(self):
        return "microsoft.graph.ResourceSpecificPermission"
