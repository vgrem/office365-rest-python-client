from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata, version


@version("beta")
class WindowsAutopilotSettings(Entity):
    @odata(name="lastManualSyncTriggerDateTime")
    @property
    def last_manual_sync_trigger_date_time(self) -> Optional[datetime]:
        """Gets the lastManualSyncTriggerDateTime property"""
        return self.properties.get("lastManualSyncTriggerDateTime", None)

    @odata(name="lastSyncDateTime")
    @property
    def last_sync_date_time(self) -> Optional[datetime]:
        """Gets the lastSyncDateTime property"""
        return self.properties.get("lastSyncDateTime", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsAutopilotSettings"

    @require_permission(
        delegated=[
            "DeviceManagementServiceConfig.ReadWrite.All",
        ],
        application=[
            "DeviceManagementServiceConfig.ReadWrite.All",
        ],
    )
    def sync(self) -> Self:
        """sync operation."""
        qry = ServiceOperationQuery(self, "sync", None, {}, None, None)
        self.context.add_query(qry)
        return self
