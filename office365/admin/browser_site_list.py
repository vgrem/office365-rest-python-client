from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.identity_set import IdentitySet
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.browser.siteliststatus import BrowserSiteListStatus
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.admin.browser_shared_cookie import BrowserSharedCookie
    from office365.admin.browser_site import BrowserSite


class BrowserSiteList(Entity):
    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> IdentitySet:
        """Gets the lastModifiedBy property"""
        return self.properties.get("lastModifiedBy", IdentitySet())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="publishedBy")
    @property
    def published_by(self) -> IdentitySet:
        """Gets the publishedBy property"""
        return self.properties.get("publishedBy", IdentitySet())

    @odata(name="publishedDateTime")
    @property
    def published_date_time(self) -> Optional[datetime]:
        """Gets the publishedDateTime property"""
        return self.properties.get("publishedDateTime", datetime.min)

    @odata(name="revision")
    @property
    def revision(self) -> Optional[str]:
        """Gets the revision property"""
        return self.properties.get("revision", None)

    @odata(name="status")
    @property
    def status(self) -> BrowserSiteListStatus:
        """Gets the status property"""
        return self.properties.get("status", BrowserSiteListStatus.draft)

    @odata(name="sharedCookies", navigation=True)
    @property
    def shared_cookies(self) -> EntityCollection[BrowserSharedCookie]:
        """Gets the sharedCookies property"""
        from office365.admin.browser_shared_cookie import BrowserSharedCookie

        return self.properties.get(
            "sharedCookies",
            EntityCollection[BrowserSharedCookie](
                self.context, BrowserSharedCookie, ResourcePath("sharedCookies", self.resource_path)
            ),
        )

    @odata(name="sites", navigation=True)
    @property
    def sites(self) -> EntityCollection[BrowserSite]:
        """Gets the sites property"""
        from office365.admin.browser_site import BrowserSite

        return self.properties.get(
            "sites", EntityCollection[BrowserSite](self.context, BrowserSite, ResourcePath("sites", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BrowserSiteList"
