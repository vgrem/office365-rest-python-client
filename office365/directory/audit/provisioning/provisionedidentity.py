from office365.directory.audit.provisioning.detailsinfo import DetailsInfo
from office365.runtime.client_value import ClientValue


class ProvisionedIdentity(ClientValue):

    def __init__(self, details: DetailsInfo = DetailsInfo(), identity_type: str = None):
        self.details = details
        self.identityType = identity_type

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisionedIdentity"
