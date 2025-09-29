from office365.runtime.client_value import ClientValue
from office365.sharepoint.directory.groupnamevalidationresulterrorparams import (
    GroupNameValidationResultErrorParams,
)


class GroupNameValidationResult(ClientValue):

    def __init__(
        self,
        alias_error_details: GroupNameValidationResultErrorParams = GroupNameValidationResultErrorParams(),
        display_name_error_details: GroupNameValidationResultErrorParams = GroupNameValidationResultErrorParams(),
        error_code: str = None,
        error_message: str = None,
        is_valid_name: bool = None,
    ):
        self.AliasErrorDetails = alias_error_details
        self.DisplayNameErrorDetails = display_name_error_details
        self.ErrorCode = error_code
        self.ErrorMessage = error_message
        self.IsValidName = is_valid_name
