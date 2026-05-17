from office365.runtime.client_value import ClientValue
from typing import Optional


class GroupNameValidationResultErrorParams(ClientValue):
    def __init__(
        self,
        blocked_word: Optional[str] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        validation_error_code: Optional[str] = None,
        validation_error_message: Optional[str] = None,
        validation_property_name: Optional[str] = None,
    ):
        self.BlockedWord = blocked_word
        self.Prefix = prefix
        self.Suffix = suffix
        self.ValidationErrorCode = validation_error_code
        self.ValidationErrorMessage = validation_error_message
        self.ValidationPropertyName = validation_property_name

    @property
    def entity_type_name(self):
        return "SP.Directory.GroupNameValidationResultErrorParams"
