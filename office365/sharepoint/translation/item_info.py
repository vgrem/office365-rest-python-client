from uuid import UUID

from office365.runtime.client_value import ClientValue


class TranslationItemInfo(ClientValue):
    """The TranslationItemInfo type contains information about a previously submitted translation item."""

    def __init__(
        self,
        translation_id=None,
        canceled: bool = None,
        error_message: str = None,
        failed: bool = None,
        in_progress: bool = None,
        input_file: str = None,
        not_started: bool = None,
        output_file: str = None,
        result: int = None,
        succeeded: bool = None,
    ):
        """
        :param str translation_id: If this translation item belongs to an immediate translation job,
            this property MUST be ignored. Otherwise, this property contains an identifier uniquely identifying
            this translation item.
        """
        super(TranslationItemInfo, self).__init__()
        self.TranslationId = translation_id
        self.Canceled = canceled
        self.ErrorMessage = error_message
        self.Failed = failed
        self.InProgress = in_progress
        self.InputFile = input_file
        self.NotStarted = not_started
        self.OutputFile = output_file
        self.Result = result
        self.Succeeded = succeeded

    @property
    def entity_type_name(self):
        return "SP.Translation.TranslationItemInfo"
