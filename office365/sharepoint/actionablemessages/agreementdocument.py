from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class AgreementDocument(ClientValue):

    def __init__(
        self,
        document_type: str = None,
        document_url: str = None,
        is_active: bool = None,
        linked_pd_fs: StringCollection = StringCollection(),
        state: str = None,
    ):
        self.DocumentType = document_type
        self.DocumentUrl = document_url
        self.IsActive = is_active
        self.LinkedPDFs = linked_pd_fs
        self.State = state
