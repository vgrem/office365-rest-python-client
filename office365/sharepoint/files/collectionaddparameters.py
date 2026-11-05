from __future__ import annotations

from office365.runtime.client_value import ClientValue


class FileCollectionAddParameters(ClientValue):
    AutoCheckoutOnInvalidData: bool | None = None
    EnsureUniqueFileName: bool | None = None
    Overwrite: bool | None = None
    XorHash: str | None = None
