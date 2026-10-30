from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.local_credential import DeviceLocalCredential
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class DeviceLocalCredentialInfo(Entity):
    """Represents local administrator credential information for all device objects in Azure Active Directory
    that are enabled with Local Admin Password Solution (LAPS)."""

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """
        Display name of the device that the local credentials are associated with.
        """
        return self.properties.get("deviceName", None)

    @odata(name="lastBackupDateTime")
    @property
    def last_backup_datetime(self):
        """When the local administrator account credential was backed up to Azure Active Directory."""
        return self.properties.get("lastBackupDateTime", datetime.min)

    @odata(name="refreshDateTime")
    @property
    def refresh_datetime(self):
        """When the local administrator account credential will be refreshed and backed up to Azure Active Directory."""
        return self.properties.get("refreshDateTime", datetime.min)

    @odata(name="credentials")
    @property
    def credentials(self) -> ClientValueCollection[DeviceLocalCredential]:
        """Gets the credentials property"""
        return self.properties.get("credentials", ClientValueCollection[DeviceLocalCredential](DeviceLocalCredential))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceLocalCredentialInfo"
