from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.backuprestore.restoresessions.browser_shared_cookie_history import (
        BrowserSharedCookieHistory,
    )
    from office365.directory.identity_set import IdentitySet
    from office365.intune.browser.sharedcookiesourceenvironment import (
        BrowserSharedCookieSourceEnvironment,
    )
    from office365.intune.browser.sharedcookiestatus import BrowserSharedCookieStatus


class BrowserSharedCookie(Entity):
    @odata(name="comment")
    @property
    def comment(self) -> Optional[str]:
        """Gets the comment property"""
        return self.properties.get("comment", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="deletedDateTime")
    @property
    def deleted_date_time(self) -> Optional[datetime]:
        """Gets the deletedDateTime property"""
        return self.properties.get("deletedDateTime", datetime.min)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="history")
    @property
    def history(self) -> ClientValueCollection[BrowserSharedCookieHistory]:
        """Gets the history property"""
        from office365.backuprestore.restoresessions.browser_shared_cookie_history import (
            BrowserSharedCookieHistory,
        )

        return self.properties.get(
            "history", ClientValueCollection[BrowserSharedCookieHistory](BrowserSharedCookieHistory)
        )

    @odata(name="hostOnly")
    @property
    def host_only(self) -> Optional[bool]:
        """Gets the hostOnly property"""
        return self.properties.get("hostOnly", None)

    @odata(name="hostOrDomain")
    @property
    def host_or_domain(self) -> Optional[str]:
        """Gets the hostOrDomain property"""
        return self.properties.get("hostOrDomain", None)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> IdentitySet:
        """Gets the lastModifiedBy property"""
        from office365.directory.identity_set import IdentitySet

        return self.properties.get("lastModifiedBy", IdentitySet())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="path")
    @property
    def path(self) -> Optional[str]:
        """Gets the path property"""
        return self.properties.get("path", None)

    @odata(name="sourceEnvironment")
    @property
    def source_environment(self) -> BrowserSharedCookieSourceEnvironment:
        """Gets the sourceEnvironment property"""
        from office365.intune.browser.sharedcookiesourceenvironment import (
            BrowserSharedCookieSourceEnvironment,
        )

        return self.properties.get("sourceEnvironment", BrowserSharedCookieSourceEnvironment.microsoftEdge)

    @odata(name="status")
    @property
    def status(self) -> BrowserSharedCookieStatus:
        """Gets the status property"""
        from office365.intune.browser.sharedcookiestatus import (
            BrowserSharedCookieStatus,
        )

        return self.properties.get("status", BrowserSharedCookieStatus.published)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BrowserSharedCookie"
