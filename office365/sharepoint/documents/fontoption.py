from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class FontOption(ClientValue):
    fontFace: str | None = None
    fontFamilyKey: str | None = None
    fontVariantWeight: str | None = None
