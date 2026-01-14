from typing import Optional

from office365.sharepoint.entity import Entity


class FeedVideoPage(Entity):
    @property
    def modern_audience_target_user_field(self) -> Optional[str]:
        """Gets the ModernAudienceTargetUserField property"""
        return self.properties.get("ModernAudienceTargetUserField", None)

    @property
    def video_duration(self) -> Optional[int]:
        """Gets the VideoDuration property"""
        return self.properties.get("VideoDuration", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.FeedVideoPage"
