from __future__ import annotations

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.key_value_pair import KeyValuePair


class ManagedAppConfiguration(Entity):
    @property
    def custom_settings(self) -> ClientValueCollection[KeyValuePair]:
        """Gets the customSettings property"""
        return self.properties.get("customSettings", ClientValueCollection[KeyValuePair](KeyValuePair))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedAppConfiguration"
