from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.mount.placesuserentity import PlacesUserEntity

if TYPE_CHECKING:
    from office365.sharepoint.mount.placesentity import PlacesEntity


class PlacesInformation(Entity):
    @odata(name="inCallersDrive")
    @property
    def in_callers_drive(self) -> Optional[str]:
        """Gets the inCallersDrive property"""
        return self.properties.get("inCallersDrive", None)

    @odata(name="placesCount")
    @property
    def places_count(self) -> Optional[str]:
        """Gets the placesCount property"""
        return self.properties.get("placesCount", None)

    @odata(name="itemSourceListTitle")
    @property
    def item_source_list_title(self) -> Optional[str]:
        """Gets the itemSourceListTitle property"""
        return self.properties.get("itemSourceListTitle", None)

    @odata(name="itemSourcePath")
    @property
    def item_source_path(self) -> Optional[str]:
        """Gets the itemSourcePath property"""
        return self.properties.get("itemSourcePath", None)

    @odata(name="itemSourceSiteOwnerIdentity")
    @property
    def item_source_site_owner_identity(self) -> PlacesUserEntity:
        """Gets the itemSourceSiteOwnerIdentity property"""
        return self.properties.get("itemSourceSiteOwnerIdentity", PlacesUserEntity())

    @odata(name="itemSourceSiteTemplateId")
    @property
    def item_source_site_template_id(self) -> Optional[str]:
        """Gets the itemSourceSiteTemplateId property"""
        return self.properties.get("itemSourceSiteTemplateId", None)

    @odata(name="itemSourceSiteTitle")
    @property
    def item_source_site_title(self) -> Optional[str]:
        """Gets the itemSourceSiteTitle property"""
        return self.properties.get("itemSourceSiteTitle", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AddToOneDrive.PlacesInformation"

    @odata(name="places", navigation=True)
    @property
    def places(self) -> EntityCollection[PlacesEntity]:
        """Gets the places property"""
        from office365.sharepoint.mount.placesentity import PlacesEntity

        return self.properties.get(
            "places",
            EntityCollection[PlacesEntity](self.context, PlacesEntity, ResourcePath("places", self.resource_path)),
        )
