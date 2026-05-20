from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class LocalizedName(ClientValue):
    """
    Represents the localized name used in the term store, which identifies the name in the localized language.
    For more information, see localizedLabel.

    :param str name: The name in the localized language.
    :param str language_tag: The language tag for the label.
    """

    name: Optional[str] = None
    languageTag: str = "en-US"

    def __repr__(self):
        return f"{self.name};{self.languageTag}"

    def __str__(self):
        return self.name or ""
