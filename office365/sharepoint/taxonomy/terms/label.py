from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class Label(ClientValue):
    """
    Args:
        name: Gets the value of the current Label object.
        is_default: Indicates whether this Label object is the default label for the label's language.
        language_tag: Indicates the locale of the current Label object.
    """

    name: str | None = None
    isDefault: bool | None = None
    languageTag: str | None = None

    def __str__(self):
        return self.name or ""

    def __repr__(self):
        return f"{self.languageTag}:{self.name}"
