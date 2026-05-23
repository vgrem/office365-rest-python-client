from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class LocalizedName(ClientValue):
    """Represents the localized name used in the term store, which identifies the name in the localized language.
    For more information, see localizedLabel.

    Args:
        name: The name in the localized language.
        language_tag: The language tag for the label.
    """

    name: str | None = None
    languageTag: str = "en-US"

    def __repr__(self):
        return f"{self.name};{self.languageTag}"

    def __str__(self):
        return self.name or ""
