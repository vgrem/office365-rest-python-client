from __future__ import annotations

from office365.runtime.client_value import ClientValue


class FolderCollectionAddParameters(ClientValue):
    EnsureUniqueFileName: bool | None = None
    Overwrite: bool | None = None
