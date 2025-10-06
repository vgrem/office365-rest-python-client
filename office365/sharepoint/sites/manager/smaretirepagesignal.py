from office365.runtime.client_value import ClientValue
from office365.sharepoint.sites.manager.smaretirepageminimumagefeedbacksignal import (
    SMARetirePageMinimumAgeFeedbackSignal,
)


class SMARetirePageSignal(ClientValue):

    def __init__(
        self,
        minimum_age: SMARetirePageMinimumAgeFeedbackSignal = SMARetirePageMinimumAgeFeedbackSignal(),
    ):
        self.MinimumAge = minimum_age

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SMARetirePageSignal"
