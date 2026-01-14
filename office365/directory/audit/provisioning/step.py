from office365.directory.audit.provisioning.detailsinfo import DetailsInfo
from office365.directory.audit.provisioning.result import ProvisioningResult
from office365.directory.audit.provisioning.steptype import ProvisioningStepType
from office365.runtime.client_value import ClientValue


class ProvisioningStep(ClientValue):
    def __init__(
        self,
        description: str = None,
        details: DetailsInfo = DetailsInfo(),
        name: str = None,
        provisioning_step_type: ProvisioningStepType = ProvisioningStepType.none,
        status: ProvisioningResult = ProvisioningResult.none,
    ):
        self.description = description
        self.details = details
        self.name = name
        self.provisioningStepType = provisioning_step_type
        self.status = status

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisioningStep"
