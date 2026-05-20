from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ContentAssemblyFileInfo(ClientValue):
    file_url: Optional[str] = None
    server_redirected_embed_url: Optional[str] = None
