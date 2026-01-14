from typing import Optional

from office365.sharepoint.entity import Entity


class SPFlight(Entity):
    @property
    def configuration(self) -> Optional[str]:
        """Gets the Configuration property"""
        return self.properties.get("Configuration", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Flighting.Runtime.SPFlight"
