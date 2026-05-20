from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.root import Root
from office365.onedrive.sites.archival_details import SiteArchivalDetails
from office365.runtime.client_value import ClientValue


@dataclass
class SiteCollection(ClientValue):
    """The siteCollection resource provides more information about a site collection."""

    root: Root | None = None
    hostname: str | None = None
    dataLocationCode: str | None = None
    archivalDetails: SiteArchivalDetails | None = field(default_factory=SiteArchivalDetails)
