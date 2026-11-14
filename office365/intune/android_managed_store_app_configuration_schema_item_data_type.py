from __future__ import annotations

from enum import Enum


class AndroidManagedStoreAppConfigurationSchemaItemDataType(Enum):
    bool = "0"
    integer = "1"
    string = "2"
    choice = "3"
    multiselect = "4"
    bundle = "5"
    bundleArray = "6"
    hidden = "7"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AndroidManagedStoreAppConfigurationSchemaItemDataType"
