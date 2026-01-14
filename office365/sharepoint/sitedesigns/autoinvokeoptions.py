from office365.runtime.client_value import ClientValue


class AutoInvokeOptions(ClientValue):
    def __init__(self, show_card_on_failure: str = None):
        self.showCardOnFailure = show_card_on_failure

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.AutoInvokeOptions"
