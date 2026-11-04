from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.sites.manager.smaretirepagesignal import SMARetirePageSignal


@value
class SiteManagerSignals(ClientValue):
    RetirePageSignals: SMARetirePageSignal = field(default_factory=SMARetirePageSignal)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SiteManagerSignals"
