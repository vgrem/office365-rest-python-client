from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.managed.android.store_app_configuration_schema_item import (
    AndroidManagedStoreAppConfigurationSchemaItem,
)
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class AndroidManagedStoreAppConfigurationSchema(Entity):
    @odata(name="exampleJson")
    @property
    def example_json(self) -> Optional[bytes]:
        """Gets the exampleJson property"""
        return self.properties.get("exampleJson", None)

    @odata(name="nestedSchemaItems")
    @property
    def nested_schema_items(self) -> ClientValueCollection[AndroidManagedStoreAppConfigurationSchemaItem]:
        """Gets the nestedSchemaItems property"""
        return self.properties.get(
            "nestedSchemaItems",
            ClientValueCollection[AndroidManagedStoreAppConfigurationSchemaItem](
                AndroidManagedStoreAppConfigurationSchemaItem
            ),
        )

    @odata(name="schemaItems")
    @property
    def schema_items(self) -> ClientValueCollection[AndroidManagedStoreAppConfigurationSchemaItem]:
        """Gets the schemaItems property"""
        return self.properties.get(
            "schemaItems",
            ClientValueCollection[AndroidManagedStoreAppConfigurationSchemaItem](
                AndroidManagedStoreAppConfigurationSchemaItem
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidManagedStoreAppConfigurationSchema"
