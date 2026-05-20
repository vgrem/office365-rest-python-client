from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.workflow.exceptiondetails import ExceptionDetails


@dataclass
class LabelAccessControlData(ClientValue):
    error_details: ExceptionDetails = field(default_factory=ExceptionDetails)
    has_access_to_label: Optional[bool] = None
    principal_name: Optional[str] = None
