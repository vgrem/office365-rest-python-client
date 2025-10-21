from office365.directory.audit.provisioning.detailsinfo import DetailsInfo
from office365.runtime.client_value import ClientValue


class ProvisioningSystem(ClientValue):

    def __init__(self, details: DetailsInfo = DetailsInfo()):
        self.details = details

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisioningSystem"
