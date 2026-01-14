from datetime import datetime

from office365.runtime.client_value import ClientValue


class CreateAgreementModel(ClientValue):
    def __init__(
        self,
        agreement_id: str = None,
        agreement_source: str = None,
        documents: str = None,
        expiration_date_time: datetime = None,
        form_field_sets: str = None,
        locale: str = None,
        message: str = None,
        name: str = None,
        recipient_sets: str = None,
        signing_mode: str = None,
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
