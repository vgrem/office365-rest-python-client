from office365.runtime.client_value import ClientValue


class DlpClassificationResult(ClientValue):

    def __init__(
        self, classification_id: str = None, confidence: int = None, count: int = None
    ):
        super().__init__()
        self.ClassificationId = classification_id
        self.Confidence = confidence
        self.Count = count

    @property
    def entity_type_name(self):
        return "SP.CompliancePolicy.DlpClassificationResult"
