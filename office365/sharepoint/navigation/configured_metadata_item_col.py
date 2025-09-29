from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.navigation.configured_metadata_item import (
    ConfiguredMetadataNavigationItem,
)


class ConfiguredMetadataNavigationItemCollection(ClientValue):
    """A collection of configured metadata navigation items."""

    def __init__(self, items=ClientValueCollection(ConfiguredMetadataNavigationItem)):
        self.Items = items
