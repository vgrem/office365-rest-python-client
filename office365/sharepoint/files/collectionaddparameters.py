from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FileCollectionAddParameters(ClientValue):
    auto_checkout_on_invalid_data: bool | None = None
    ensure_unique_file_name: bool | None = None
    overwrite: bool | None = None
    xor_hash: str | None = None
