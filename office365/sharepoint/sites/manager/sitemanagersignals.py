from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sites.manager.smaretirepagesignal import SMARetirePageSignal


@dataclass
class SiteManagerSignals(ClientValue):
    RetirePageSignals: SMARetirePageSignal = field(default_factory=SMARetirePageSignal)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SiteManagerSignals"
