from __future__ import annotations

from dataclasses import field

from office365.communications.media_info import MediaInfo
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MediaPrompt(ClientValue):
    mediaInfo: MediaInfo = field(default_factory=MediaInfo)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MediaPrompt"
