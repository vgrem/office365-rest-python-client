from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.sites.manager.smaretirepageminimumagefeedbacksignal import (
    SMARetirePageMinimumAgeFeedbackSignal,
)


@value
class SMARetirePageSignal(ClientValue):
    MinimumAge: SMARetirePageMinimumAgeFeedbackSignal = field(default_factory=SMARetirePageMinimumAgeFeedbackSignal)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SMARetirePageSignal"
