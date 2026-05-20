from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ResourceVisualization(ClientValue):
    acronym: Optional[str] = None
    color: Optional[str] = None
    preview_image_url: Optional[str] = None
