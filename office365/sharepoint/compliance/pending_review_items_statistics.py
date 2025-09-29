from office365.runtime.client_value import ClientValue


class PendingReviewItemsStatistics(ClientValue):

    def __init__(
        self, label_id=None, label_name=None, pending_review_items_count: int = None
    ):
        self.LabelId = label_id
        self.LabelName = label_name
        self.PendingReviewItemsCount = pending_review_items_count

    @property
    def entity_type_name(self):
        return "SP.CompliancePolicy.PendingReviewItemsStatistics"
