from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FolderCollectionAddParameters(ClientValue):
    ensure_unique_file_name: bool | None = None
    overwrite: bool | None = None
