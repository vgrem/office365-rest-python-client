from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.internal.image_url import ImageUrl


class ImageContentPart(ClientValue):
    ImageUrl: ImageUrl = field(default_factory=ImageUrl)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Internal.ImageContentPart"
