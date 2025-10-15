from typing import Optional

from office365.sharepoint.entity import Entity


class VideoPlaybackMetadata(Entity):

    @property
    def hls_url(self) -> Optional[str]:
        """Gets the HLSUrl property"""
        return self.properties.get("HLSUrl", None)

    @property
    def sdn_playback_metadata(self) -> Optional[str]:
        """Gets the SdnPlaybackMetadata property"""
        return self.properties.get("SdnPlaybackMetadata", None)

    @property
    def streaming_url(self) -> Optional[str]:
        """Gets the StreamingUrl property"""
        return self.properties.get("StreamingUrl", None)

    @property
    def token(self) -> Optional[str]:
        """Gets the Token property"""
        return self.properties.get("Token", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.VideoPlaybackMetadata"
