from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class TranslationItemInfo(ClientValue):
    """The TranslationItemInfo type contains information about a previously submitted translation item.

    translation_id: If this translation item belongs to an immediate translation job,
        this property MUST be ignored. Otherwise, this property contains an identifier uniquely identifying
        this translation item.
    """

    TranslationId: Optional[str] = None
    Canceled: Optional[bool] = None
    ErrorMessage: Optional[str] = None
    Failed: Optional[bool] = None
    InProgress: Optional[bool] = None
    InputFile: Optional[str] = None
    NotStarted: Optional[bool] = None
    OutputFile: Optional[str] = None
    Result: Optional[int] = None
    Succeeded: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Translation.TranslationItemInfo"
