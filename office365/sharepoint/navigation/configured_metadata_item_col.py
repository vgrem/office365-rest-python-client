from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.navigation.configured_metadata_item import (
    ConfiguredMetadataNavigationItem,
)


class ConfiguredMetadataNavigationItemCollection(ClientValue):
    """A collection of configured metadata navigation items."""

    Items: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(ConfiguredMetadataNavigationItem))

    @property
    def entity_type_name(self) -> str:
        return "SP.MetadataNavigation.ConfiguredMetadataNavigationItemCollection"
