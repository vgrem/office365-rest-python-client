from office365.runtime.client_value import ClientValue


class InitializeAgreementModel(ClientValue):
    def __init__(self, agreement_id: str = None, documents: str = None):
        self.agreementId = agreement_id
        self.documents = documents

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.InitializeAgreementModel"
