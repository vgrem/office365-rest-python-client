from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.security.cloud_clipboard_item_payload import CloudClipboardItemPayload


class CloudClipboardItem(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="expirationDateTime")
    @property
    def expiration_date_time(self) -> Optional[datetime]:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="payloads")
    @property
    def payloads(self) -> ClientValueCollection[CloudClipboardItemPayload]:
        """Gets the payloads property"""
        return self.properties.get(
            "payloads", ClientValueCollection[CloudClipboardItemPayload](CloudClipboardItemPayload)
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudClipboardItem"
