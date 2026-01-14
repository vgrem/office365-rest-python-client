from office365.runtime.client_value import ClientValue


class LinkParameters(ClientValue):
    def __init__(self, nav: str = None):
        self.nav = nav

    @property
    def entity_type_name(self):
        return "SP.Sharing.LinkParameters"
