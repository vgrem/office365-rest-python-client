from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class FileCollectionAddParameters(ClientValue):
    AutoCheckoutOnInvalidData: bool | None = None
    EnsureUniqueFileName: bool | None = None
    Overwrite: bool | None = None
    XorHash: str | None = None
