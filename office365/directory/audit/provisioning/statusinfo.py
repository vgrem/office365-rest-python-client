from office365.directory.audit.provisioning.errorinfo import ProvisioningErrorInfo
from office365.directory.audit.provisioning.result import ProvisioningResult
from office365.runtime.client_value import ClientValue


class ProvisioningStatusInfo(ClientValue):
    def __init__(
        self,
        error_information: ProvisioningErrorInfo = ProvisioningErrorInfo(),
        status: ProvisioningResult = None,
    ):
        self.errorInformation = error_information
        self.status = status

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisioningStatusInfo"
