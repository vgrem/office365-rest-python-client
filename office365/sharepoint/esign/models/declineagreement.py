from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class DeclineAgreementModel(ClientValue):
    documentId: Optional[str] = None
    reason: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.DeclineAgreementModel"
