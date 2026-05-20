from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TemporaryFolderFileInfo(ClientValue):
    dummy_file_url: str | None = None
    server_redirected_embed_url: str | None = None
    temporary_file_url: str | None = None
