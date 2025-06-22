from typing import Optional

from office365.sharepoint.changes.change import Change


class ChangeGroup(Change):
    """Specifies a change on a group."""

    @property
    def group_id(self) -> Optional[int]:
        """Identifies the changed group."""
        return self.properties.get("GroupId", None)
