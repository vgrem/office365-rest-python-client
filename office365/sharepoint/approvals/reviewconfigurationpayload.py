from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class ReviewConfigurationPayload(ClientValue):
    def __init__(
        self,
        category_id: str = None,
        reviewers: StringCollection = StringCollection(),
        review_type: str = None,
    ):
        self.category_id = category_id
        self.reviewers = reviewers
        self.review_type = review_type
