from office365.runtime.client_value import ClientValue


class PreservedCloudAttachment(ClientValue):
    def __init__(self, composite_document_id: str = None, url: str = None):
        self.CompositeDocumentId = composite_document_id
        self.Url = url

    @property
    def entity_type_name(self):
        return "SP.ComplianceFoundation.Models.PreservedCloudAttachment"
