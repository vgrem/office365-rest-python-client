from typing import Optional

from office365.sharepoint.entity import Entity


class FollowedItemData(Entity):
    @property
    def properties(self) -> Optional[dict]:  # type: ignore[override]
        """Gets the Properties property"""
        return super().properties.get("Properties", None)

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.FollowedItemData"
