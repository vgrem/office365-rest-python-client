from office365.runtime.client_value import ClientValue


class WebAppExtUrlPair(ClientValue):

    def __init__(self, ext: str = None, wac_url: str = None):
        self.Ext = ext
        self.WacUrl = wac_url

    @property
    def entity_type_name(self):
        return "SP.Utilities.WebAppExtUrlPair"
