from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.document import AgreementDocument


class AgreementDocumentsInfo(ClientValue):
    def __init__(self, documents: ClientValueCollection[AgreementDocument] = None):
        self.documents = documents
