from office365.runtime.client_value import ClientValue
from typing import Optional


class CompleteAgreementModel(ClientValue):
    def __init__(
        self,
        document_id: Optional[str] = None,
        original_doc_name: Optional[str] = None,
        target_folder_uri: Optional[str] = None,
    ):
        self.documentId = document_id
        self.originalDocName = original_doc_name
        self.targetFolderUri = target_folder_uri

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.CompleteAgreementModel"
