from office365.runtime.client_value import ClientValue
from office365.sharepoint.workflow.exceptiondetails import ExceptionDetails


class LabelAccessControlData(ClientValue):

    def __init__(
        self,
        error_details: ExceptionDetails = ExceptionDetails(),
        has_access_to_label: bool = None,
        principal_name: str = None,
    ):
        self.error_details = error_details
        self.has_access_to_label = has_access_to_label
        self.principal_name = principal_name
