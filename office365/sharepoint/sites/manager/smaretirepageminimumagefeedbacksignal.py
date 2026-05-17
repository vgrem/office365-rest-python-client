from office365.runtime.client_value import ClientValue
from typing import Optional


class SMARetirePageMinimumAgeFeedbackSignal(ClientValue):
    def __init__(
        self,
        default_age: Optional[int] = None,
        from_dismiss_action: Optional[int] = None,
        from_empty_state: Optional[int] = None,
        preferred_age: Optional[int] = None,
    ):
        self.DefaultAge = default_age
        self.FromDismissAction = from_dismiss_action
        self.FromEmptyState = from_empty_state
        self.PreferredAge = preferred_age

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SMARetirePageMinimumAgeFeedbackSignal"
