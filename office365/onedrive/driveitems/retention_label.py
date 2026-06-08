from datetime import datetime
from typing import Optional

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.onedrive.driveitems.retention_label_settings import (
    RetentionLabelSettings,
)
from office365.runtime.types.odata_property import odata


class ItemRetentionLabel(Entity):
    """
    Groups retention and compliance-related properties on an item into a single structure.
    Currently, supported only for driveItem.
    """

    @property
    def is_label_applied_explicitly(self) -> Optional[bool]:
        """Specifies whether the label is applied explicitly on the item.
        True indicates that the label is applied explicitly; otherwise, the label is inherited from its parent.
        Read-only."""
        return self.properties.get("isLabelAppliedExplicitly", None)

    @property
    def label_applied_by(self) -> Optional[IdentitySet]:
        """Identity of the user who applied the label. Read-only."""
        return self.properties.get("labelAppliedBy", IdentitySet())

    @odata(name="labelAppliedDateTime")
    @property
    def label_applied_datetime(self) -> Optional[datetime]:
        """The date and time when the label was applied on the item.
        The timestamp type represents date and time information using ISO 8601 format and is always in UTC.
        """
        return self.properties.get("labelAppliedDateTime", datetime.min)

    @property
    def name(self) -> Optional[str]:
        """The retention label on the document. Read-write."""
        return self.properties.get("name", None)

    @name.setter
    def name(self, value: str):
        """Sets the retention label on the document"""
        self.set_property("name", value)

    @odata(name="retentionSettings")
    @property
    def retention_settings(self) -> RetentionLabelSettings:
        """The retention settings enforced on the item. Read-write."""
        return self.properties.get("retentionSettings", RetentionLabelSettings())
