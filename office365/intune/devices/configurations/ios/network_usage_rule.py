from __future__ import annotations

from dataclasses import field

from office365.intune.devices.management.mobileapps.app_list_item import AppListItem
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value


@value
class IosNetworkUsageRule(ClientValue):
    cellularDataBlocked: bool | None = None
    cellularDataBlockWhenRoaming: bool | None = None
    managedApps: ClientValueCollection[AppListItem] = field(default_factory=lambda: ClientValueCollection(AppListItem))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IosNetworkUsageRule"
