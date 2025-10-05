from office365.runtime.client_value import ClientValue


class XSSearchPolicy(ClientValue):

    def __init__(self, policy: str = None):
        self.Policy = policy

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.XSSearchPolicy"
