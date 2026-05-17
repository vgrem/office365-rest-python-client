from typing import Optional

from office365.runtime.client_value import ClientValue


class TranslationItemInfo(ClientValue):
    """The TranslationItemInfo type contains information about a previously submitted translation item."""

    def __init__(
        self,
        translation_id=None,
        canceled: Optional[bool] = None,
        error_message: Optional[str] = None,
        failed: Optional[bool] = None,
        in_progress: Optional[bool] = None,
        input_file: Optional[str] = None,
        not_started: Optional[bool] = None,
        output_file: Optional[str] = None,
        result: Optional[int] = None,
        succeeded: Optional[bool] = None,
    ):
        """
        :param str translation_id: If this translation item belongs to an immediate translation job,
            this property MUST be ignored. Otherwise, this property contains an identifier uniquely identifying
            this translation item.
        """
        super().__init__()
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
