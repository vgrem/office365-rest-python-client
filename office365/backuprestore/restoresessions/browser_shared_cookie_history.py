from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.directory.permissions.identity_set import IdentitySet
from office365.intune.browser.sharedcookiesourceenvironment import BrowserSharedCookieSourceEnvironment
from office365.runtime.client_value import ClientValue


@dataclass
class BrowserSharedCookieHistory(ClientValue):
    comment: str | None = None
    displayName: str | None = None
    hostOnly: bool | None = None
    hostOrDomain: str | None = None
    lastModifiedBy: IdentitySet = field(default_factory=IdentitySet)
    path: str | None = None
    publishedDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    sourceEnvironment: BrowserSharedCookieSourceEnvironment = BrowserSharedCookieSourceEnvironment.microsoftEdge

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BrowserSharedCookieHistory"
