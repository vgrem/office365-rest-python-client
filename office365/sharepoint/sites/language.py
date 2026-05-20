from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class Language(ClientValue):
    """Represents a natural language.

    Fields:
        DisplayName: Specifies the name of the language as displayed in the user interface.
        LanguageTag: Specifies the corresponding culture name for the language.
        Lcid: Specifies the language code identifier (LCID) for the language.
    """

    DisplayName: Optional[str] = None
    LanguageTag: Optional[str] = None
    Lcid: Optional[int] = None

    def __str__(self):
        return self.DisplayName or ""

    def __repr__(self):
        return f"{self.DisplayName or ''}: {self.LanguageTag or ''}"
