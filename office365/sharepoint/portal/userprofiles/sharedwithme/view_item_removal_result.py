from office365.runtime.client_value import ClientValue


class SharedWithMeViewItemRemovalResult(ClientValue):

    def __init__(
        self, error_code: int = None, error_message: str = None, success: bool = None
    ):
        self.ErrorCode = error_code
        self.ErrorMessage = error_message
        self.Success = success

    "An object that contains the result of calling the API to remove an item from a user's 'Shared With Me' view."

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharedWithMeViewItemRemovalResult"
