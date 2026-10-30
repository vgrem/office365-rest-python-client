from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SiteDesignRun(Entity):
    @odata(name="SiteDesignID", beta=True)
    @property
    def site_design_id(self) -> Optional[str]:
        """"""
        return self.properties.get("SiteDesignID", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignRun"

    @odata(name="ActionTrigger", beta=True)
    @property
    def action_trigger(self) -> Optional[int]:
        """Gets the ActionTrigger property"""
        return self.properties.get("ActionTrigger", None)

    @odata(name="ID", beta=True)
    @property
    def id(self) -> Optional[UUID]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    @odata(name="InvokedBy", beta=True)
    @property
    def invoked_by(self) -> Optional[str]:
        """Gets the InvokedBy property"""
        return self.properties.get("InvokedBy", None)

    @odata(name="SiteDesignTitle", beta=True)
    @property
    def site_design_title(self) -> Optional[str]:
        """Gets the SiteDesignTitle property"""
        return self.properties.get("SiteDesignTitle", None)

    @odata(name="SiteDesignVersion", beta=True)
    @property
    def site_design_version(self) -> Optional[int]:
        """Gets the SiteDesignVersion property"""
        return self.properties.get("SiteDesignVersion", None)

    @odata(name="SiteID", beta=True)
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteID property"""
        return self.properties.get("SiteID", None)

    @odata(name="StartTime", beta=True)
    @property
    def start_time(self) -> Optional[int]:
        """Gets the StartTime property"""
        return self.properties.get("StartTime", None)

    @odata(name="WebID", beta=True)
    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the WebID property"""
        return self.properties.get("WebID", None)
