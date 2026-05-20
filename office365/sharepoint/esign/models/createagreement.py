from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CreateAgreementModel(ClientValue):
    agreementId: Optional[str] = None
    agreementSource: Optional[str] = None
    documents: Optional[str] = None
    expirationDateTime: Optional[datetime] = None
    formFieldSets: Optional[str] = None
    locale: Optional[str] = None
    message: Optional[str] = None
    name: Optional[str] = None
    recipientSets: Optional[str] = None
    signingMode: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.CreateAgreementModel"
