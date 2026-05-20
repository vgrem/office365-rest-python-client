from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class UploadDocumentInfo(ClientValue):
    agreement_library_id: Optional[str] = None
    file_item_id: Optional[int] = None
    file_name: Optional[str] = None
    file_server_redirected_embed_url: Optional[str] = None
    file_server_relative_url: Optional[str] = None
    file_unique_id: Optional[str] = None
    folder_item_id: Optional[int] = None
    folder_server_relative_url: Optional[str] = None
