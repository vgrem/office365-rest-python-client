from typing import Optional

from office365.sharepoint.entity import Entity


class GeoExperience(Entity):
    @property
    def geo_location(self) -> Optional[str]:
        """Gets the GeoLocation property"""
        return self.properties.get("GeoLocation", None)

    @property
    def multi_geo_experience_mode(self) -> Optional[int]:
        """Gets the MultiGeoExperienceMode property"""
        return self.properties.get("MultiGeoExperienceMode", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.GeoExperience"
