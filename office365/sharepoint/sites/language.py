from typing import Optional

from office365.runtime.client_value import ClientValue


class Language(ClientValue):
    """Represents a natural language."""

    def __init__(
        self, display_name: Optional[str] = None, language_tag: Optional[str] = None, lcid: Optional[int] = None
    ):
        """
        :param str display_name: Specifies the name of the language as displayed in the user interface.
        :param str language_tag: Specifies the corresponding culture name for the language.
        :param int lcid: Specifies the language code identifier (LCID) for the language.
        """
        self.DisplayName = display_name
        self.LanguageTag = language_tag
        self.Lcid = lcid

    def __str__(self):
        return self.DisplayName or ""

    def __repr__(self):
        return f"{self.DisplayName or ''}: {self.LanguageTag or ''}"
