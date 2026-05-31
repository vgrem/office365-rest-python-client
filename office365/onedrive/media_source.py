from __future__ import annotations

from dataclasses import dataclass

from office365.onedrive.driveitems.mediasourcecontentcategory import MediaSourceContentCategory
from office365.runtime.client_value import ClientValue


@dataclass
class MediaSource(ClientValue):
    contentCategory: MediaSourceContentCategory = MediaSourceContentCategory.meeting

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MediaSource"
