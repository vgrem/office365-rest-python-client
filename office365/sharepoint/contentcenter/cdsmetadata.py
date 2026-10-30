from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class CDSMetadata(Entity):
    @odata(name="FriendlyName", beta=True)
    @property
    def friendly_name(self) -> Optional[str]:
        """Gets the FriendlyName property"""
        return self.properties.get("FriendlyName", None)

    @odata(name="InstanceUrl", beta=True)
    @property
    def instance_url(self) -> Optional[str]:
        """Gets the InstanceUrl property"""
        return self.properties.get("InstanceUrl", None)

    @odata(name="ResourceId", beta=True)
    @property
    def resource_id(self) -> Optional[str]:
        """Gets the ResourceId property"""
        return self.properties.get("ResourceId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.CDSMetadata"
