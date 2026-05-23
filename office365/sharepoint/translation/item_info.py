from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TranslationItemInfo(ClientValue):
    """The TranslationItemInfo type contains information about a previously submitted translation item.

    Fields:
        TranslationId: If this translation item belongs to an immediate translation job,
            this property MUST be ignored. Otherwise, this property contains an identifier
            uniquely identifying this translation item.
    """

    TranslationId: str | None = None
    Canceled: bool | None = None
    ErrorMessage: str | None = None
    Failed: bool | None = None
    InProgress: bool | None = None
    InputFile: str | None = None
    NotStarted: bool | None = None
    OutputFile: str | None = None
    Result: int | None = None
    Succeeded: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "SP.Translation.TranslationItemInfo"
