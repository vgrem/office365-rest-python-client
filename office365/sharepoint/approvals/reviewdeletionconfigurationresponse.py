from office365.runtime.client_value import ClientValue


class ReviewDeletionConfigurationResponse(ClientValue):
    def __init__(self, action: str = None, contract_category_id: str = None, message: str = None):
        self.action = action
        self.contract_category_id = contract_category_id
        self.message = message
