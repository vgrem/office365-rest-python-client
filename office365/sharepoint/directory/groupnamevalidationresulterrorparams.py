from office365.runtime.client_value import ClientValue


class GroupNameValidationResultErrorParams(ClientValue):

    def __init__(
        self,
        blocked_word: str = None,
        prefix: str = None,
        suffix: str = None,
        validation_error_code: str = None,
        validation_error_message: str = None,
        validation_property_name: str = None,
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
