from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.protection.volumetype import VolumeType


class BitlockerRecoveryKey(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="key")
    @property
    def key(self) -> Optional[str]:
        """Gets the key property"""
        return self.properties.get("key", None)

    @odata(name="volumeType")
    @property
    def volume_type(self) -> VolumeType:
        """Gets the volumeType property"""
        from office365.directory.protection.volumetype import VolumeType

        return self.properties.get("volumeType", VolumeType.operatingSystemVolume)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BitlockerRecoveryKey"
