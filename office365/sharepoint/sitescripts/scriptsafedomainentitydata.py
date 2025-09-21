from office365.runtime.client_value import ClientValue


class ScriptSafeDomainEntityData(ClientValue):

    def __init__(self, domain_name: str = None):
        self.domain_name = domain_name
