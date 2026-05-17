from __future__ import annotations

from office365.runtime.client_value import ClientValue


class LocalizedDescription(ClientValue):
    """Represents the localized description used to describe a term in the term store."""

    def __init__(self, language_tag: str | None = None, description: str | None = None):
        """
        :param str language_tag: The language tag for the label.
        :param str description: The description in the localized language.
        """
        super().__init__()
        self.languageTag = language_tag
        self.description = description
