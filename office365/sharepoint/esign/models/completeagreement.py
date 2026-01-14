from office365.runtime.client_value import ClientValue


class CompleteAgreementModel(ClientValue):
    def __init__(
        self,
        document_id: str = None,
        original_doc_name: str = None,
        target_folder_uri: str = None,
    ):
        self.documentId = document_id
        self.originalDocName = original_doc_name
        self.targetFolderUri = target_folder_uri

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.CompleteAgreementModel"
