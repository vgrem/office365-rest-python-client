from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class AgreementDocument(ClientValue):
    def __init__(
        self,
        document_type: Optional[str] = None,
        document_url: Optional[str] = None,
        is_active: Optional[bool] = None,
        linked_pd_fs: StringCollection = StringCollection(),
        state: Optional[str] = None,
    ):
        self.DocumentType = document_type
        self.DocumentUrl = document_url
        self.IsActive = is_active
        self.LinkedPDFs = linked_pd_fs
        self.State = state
