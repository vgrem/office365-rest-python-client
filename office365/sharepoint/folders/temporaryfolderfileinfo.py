from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TemporaryFolderFileInfo(ClientValue):
    DummyFileUrl: str | None = None
    ServerRedirectedEmbedUrl: str | None = None
    TemporaryFileUrl: str | None = None
