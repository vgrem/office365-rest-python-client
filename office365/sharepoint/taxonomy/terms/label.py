from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class Label(ClientValue):
    """
    :param str name: 	Gets the value of the current Label object.
    :param bool is_default: Indicates whether this Label object is the default label for the label's language.
    :param str language_tag: Indicates the locale of the current Label object.
    """

    name: Optional[str] = None
    isDefault: Optional[bool] = None
    languageTag: Optional[str] = None

    def __str__(self):
        return self.name or ""

    def __repr__(self):
        return f"{self.languageTag}:{self.name}"
