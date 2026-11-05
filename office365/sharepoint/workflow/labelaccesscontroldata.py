from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.workflow.exceptiondetails import ExceptionDetails


class LabelAccessControlData(ClientValue):
    ErrorDetails: ExceptionDetails = field(default_factory=ExceptionDetails)
    HasAccessToLabel: bool | None = None
    PrincipalName: str | None = None
