from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class CreateAgreementModel(ClientValue):
    def __init__(
        self,
        agreement_id: Optional[str] = None,
        agreement_source: Optional[str] = None,
        documents: Optional[str] = None,
        expiration_date_time: Optional[datetime] = None,
        form_field_sets: Optional[str] = None,
        locale: Optional[str] = None,
        message: Optional[str] = None,
        name: Optional[str] = None,
        recipient_sets: Optional[str] = None,
        signing_mode: Optional[str] = None,
    ):
        self.agreementId = agreement_id
        self.agreementSource = agreement_source
        self.documents = documents
        self.expirationDateTime = expiration_date_time
        self.formFieldSets = form_field_sets
        self.locale = locale
        self.message = message
        self.name = name
        self.recipientSets = recipient_sets
        self.signingMode = signing_mode

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.CreateAgreementModel"
