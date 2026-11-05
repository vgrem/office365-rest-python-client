from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TemporaryFolderFileInfo(ClientValue):
    DummyFileUrl: str | None = None
    ServerRedirectedEmbedUrl: str | None = None
    TemporaryFileUrl: str | None = None
