from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.directory.permissions.identity_set import IdentitySet
from office365.intune.browser.sitecompatibilitymode import BrowserSiteCompatibilityMode
from office365.intune.browser.sitemergetype import BrowserSiteMergeType
from office365.intune.browser.sitetargetenvironment import BrowserSiteTargetEnvironment
from office365.runtime.client_value import ClientValue


@dataclass
class BrowserSiteHistory(ClientValue):
    allowRedirect: bool | None = None
    comment: str | None = None
    compatibilityMode: BrowserSiteCompatibilityMode = BrowserSiteCompatibilityMode.default
    lastModifiedBy: IdentitySet = field(default_factory=IdentitySet)
    mergeType: BrowserSiteMergeType = BrowserSiteMergeType.noMerge
    publishedDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    targetEnvironment: BrowserSiteTargetEnvironment = BrowserSiteTargetEnvironment.internetExplorerMode

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BrowserSiteHistory"
