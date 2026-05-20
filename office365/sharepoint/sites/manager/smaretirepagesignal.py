from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sites.manager.smaretirepageminimumagefeedbacksignal import (
    SMARetirePageMinimumAgeFeedbackSignal,
)


@dataclass
class SMARetirePageSignal(ClientValue):
    MinimumAge: SMARetirePageMinimumAgeFeedbackSignal = field(default_factory=SMARetirePageMinimumAgeFeedbackSignal)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SMARetirePageSignal"
