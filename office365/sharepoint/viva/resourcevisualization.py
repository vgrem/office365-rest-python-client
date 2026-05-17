from office365.runtime.client_value import ClientValue
from typing import Optional


class ResourceVisualization(ClientValue):
    def __init__(
        self, acronym: Optional[str] = None, color: Optional[str] = None, preview_image_url: Optional[str] = None
    ):
        self.acronym = acronym
        self.color = color
        self.preview_image_url = preview_image_url
