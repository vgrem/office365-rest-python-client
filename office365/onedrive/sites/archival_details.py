from __future__ import annotations

from dataclasses import dataclass

from office365.onedrive.sites.archivestatus import SiteArchiveStatus
from office365.runtime.client_value import ClientValue


@dataclass
class SiteArchivalDetails(ClientValue):
    archiveStatus: SiteArchiveStatus = SiteArchiveStatus.recentlyArchived
    "Represents the archival details of a siteCollection."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SiteArchivalDetails"
