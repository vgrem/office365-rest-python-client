from office365.directory.audit.provisioning.statuserrorcategory import ProvisioningStatusErrorCategory
from office365.runtime.client_value import ClientValue


class ProvisioningErrorInfo(ClientValue):

    def __init__(
        self,
        additional_details: str = None,
        error_category: ProvisioningStatusErrorCategory = ProvisioningStatusErrorCategory.none,
        error_code: str = None,
        reason: str = None,
        recommended_action: str = None,
    ):
        self.additionalDetails = additional_details
        self.errorCategory = error_category
        self.errorCode = error_code
        self.reason = reason
        self.recommendedAction = recommended_action

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProvisioningErrorInfo"
