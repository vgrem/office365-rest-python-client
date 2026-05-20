from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class InitializeAgreementModel(ClientValue):
    agreementId: Optional[str] = None
    documents: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.InitializeAgreementModel"
