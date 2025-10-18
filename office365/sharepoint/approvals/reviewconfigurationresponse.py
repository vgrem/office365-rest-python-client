from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.approvals.user import UserDTO


class ReviewConfigurationResponse(ClientValue):

    def __init__(
        self,
        action: str = None,
        contract_category: str = None,
        contract_category_id: str = None,
        reviewers: ClientValueCollection[UserDTO] = ClientValueCollection(UserDTO),
        review_type: str = None,
    ):
        self.action = action
        self.contract_category = contract_category
        self.contract_category_id = contract_category_id
        self.reviewers = reviewers
        self.review_type = review_type
