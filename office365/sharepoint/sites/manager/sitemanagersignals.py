from office365.runtime.client_value import ClientValue
from office365.sharepoint.sites.manager.smaretirepagesignal import SMARetirePageSignal


class SiteManagerSignals(ClientValue):

    def __init__(self, retire_page_signals: SMARetirePageSignal = SMARetirePageSignal()):
        self.RetirePageSignals = retire_page_signals

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SiteManager.SiteManagerSignals"
