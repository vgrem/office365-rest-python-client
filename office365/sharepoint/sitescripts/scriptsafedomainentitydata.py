from office365.runtime.client_value import ClientValue


class ScriptSafeDomainEntityData(ClientValue):
    """Microsoft.SharePoint.Client.ScriptSafeDomainEntityData is not applicable"""

    def __init__(self, domain_name: str = None):
        self.domain_name = domain_name
