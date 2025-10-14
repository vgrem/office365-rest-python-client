from typing import Optional

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.contentcenter.machinelearning.machinelearningpublicationentitydata import (
    SPMachineLearningPublicationEntityData,
)
from office365.sharepoint.entity import Entity


class SPMachineLearningPublicationsEntityData(Entity):

    @property
    def comment(self) -> Optional[str]:
        """Gets the Comment property"""
        return self.properties.get("Comment", None)

    @property
    def is_tile_view_enabled(self) -> Optional[bool]:
        """Gets the isTileViewEnabled property"""
        return self.properties.get("isTileViewEnabled", None)

    @property
    def model_site_url(self) -> Optional[str]:
        """Gets the ModelSiteUrl property"""
        return self.properties.get("ModelSiteUrl", None)

    @property
    def model_web_server_relative_url(self) -> Optional[str]:
        """Gets the ModelWebServerRelativeUrl property"""
        return self.properties.get("ModelWebServerRelativeUrl", None)

    @property
    def promote(self) -> Optional[bool]:
        """Gets the Promote property"""
        return self.properties.get("Promote", None)

    @property
    def publications(self) -> ClientValueCollection[SPMachineLearningPublicationEntityData]:
        """Gets the Publications property"""
        return self.properties.get("Publications", ClientValueCollection(SPMachineLearningPublicationEntityData))

    @property
    def publication_type(self) -> Optional[int]:
        """Gets the PublicationType property"""
        return self.properties.get("PublicationType", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningPublicationsEntityData"
