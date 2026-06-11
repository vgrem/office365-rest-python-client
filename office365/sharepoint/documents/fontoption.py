from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FontOption(ClientValue):
    fontFace: str | None = None
    fontFamilyKey: str | None = None
    fontVariantWeight: str | None = None
