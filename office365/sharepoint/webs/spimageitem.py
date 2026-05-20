from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPImageItem(ClientValue):
    name: Optional[str] = None
    server_relative_url: Optional[str] = None
    unique_id: Optional[str] = None
