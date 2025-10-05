from office365.runtime.client_value import ClientValue


class XSSearchPolicy(ClientValue):

    def __init__(self, policy: str = None):
        self.Policy = policy
