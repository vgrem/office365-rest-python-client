from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FileCollectionAddParameters(ClientValue):
    AutoCheckoutOnInvalidData: bool | None = None
    EnsureUniqueFileName: bool | None = None
    Overwrite: bool | None = None
    XorHash: str | None = None
