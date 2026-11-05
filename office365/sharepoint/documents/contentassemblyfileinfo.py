from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ContentAssemblyFileInfo(ClientValue):
    FileUrl: str | None = None
    ServerRedirectedEmbedUrl: str | None = None
