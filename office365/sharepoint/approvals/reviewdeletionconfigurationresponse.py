from typing import Optional

from office365.runtime.client_value import ClientValue


class ReviewDeletionConfigurationResponse(ClientValue):
    def __init__(
        self, action: Optional[str] = None, contract_category_id: Optional[str] = None, message: Optional[str] = None
    ):
        self.action = action
        self.contract_category_id = contract_category_id
        self.message = message
