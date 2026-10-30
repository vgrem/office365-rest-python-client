from __future__ import annotations

from typing import Optional

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.sitedesigns.metadata import SiteDesignMetadata


class DesignPackageMenuContents(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.DesignPackageMenuContents"

    @odata(name="HiddenDesignPackages", beta=True)
    @property
    def hidden_design_packages(self) -> Optional[int]:
        """Gets the HiddenDesignPackages property"""
        return self.properties.get("HiddenDesignPackages", None)

    @odata(name="SiteDesigns", beta=True)
    @property
    def site_designs(self) -> ClientValueCollection[SiteDesignMetadata]:
        """Gets the SiteDesigns property"""
        return self.properties.get("SiteDesigns", ClientValueCollection[SiteDesignMetadata](SiteDesignMetadata))
