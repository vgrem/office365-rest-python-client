from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class GptAsyncSubmitResponse(ClientValue):
    ErrorMessage: Optional[str] = None
    FailureReason: Optional[str] = None
    Status: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptAsyncSubmitResponse"
