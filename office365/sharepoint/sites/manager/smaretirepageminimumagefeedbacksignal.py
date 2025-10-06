from office365.runtime.client_value import ClientValue


class SMARetirePageMinimumAgeFeedbackSignal(ClientValue):

    def __init__(
        self,
        default_age: int = None,
        from_dismiss_action: int = None,
        from_empty_state: int = None,
        preferred_age: int = None,
    ):
        self.DefaultAge = default_age
        self.FromDismissAction = from_dismiss_action
        self.FromEmptyState = from_empty_state
        self.PreferredAge = preferred_age

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SMARetirePageMinimumAgeFeedbackSignal"
