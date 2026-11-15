from __future__ import annotations

from dataclasses import field

from office365.intune.devices.management.managed.android.store_app_configuration_schema_item_data_type import (
    AndroidManagedStoreAppConfigurationSchemaItemDataType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.key_value_pair import KeyValuePair


class AndroidManagedStoreAppConfigurationSchemaItem(ClientValue):
    dataType: AndroidManagedStoreAppConfigurationSchemaItemDataType = (
        AndroidManagedStoreAppConfigurationSchemaItemDataType.bool
    )
    defaultBoolValue: bool | None = None
    defaultIntValue: int | None = None
    defaultStringArrayValue: StringCollection = field(default_factory=StringCollection)
    defaultStringValue: str | None = None
    description: str | None = None
    displayName: str | None = None
    index: int | None = None
    parentIndex: int | None = None
    schemaItemKey: str | None = None
    selections: ClientValueCollection[KeyValuePair] = field(default_factory=lambda: ClientValueCollection(KeyValuePair))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidManagedStoreAppConfigurationSchemaItem"
