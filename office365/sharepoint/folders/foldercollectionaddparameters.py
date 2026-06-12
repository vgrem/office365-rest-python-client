from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FolderCollectionAddParameters(ClientValue):
    EnsureUniqueFileName: bool | None = None
    Overwrite: bool | None = None
