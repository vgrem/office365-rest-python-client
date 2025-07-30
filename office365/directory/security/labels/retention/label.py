from typing import Optional

from office365.directory.permissions.identity_set import IdentitySet
from office365.directory.security.labels.retention.duration import RetentionDuration
from office365.directory.security.labels.retention.trigger import RetentionTrigger
from office365.directory.security.labels.retention.types import (
    BehaviorDuringRetentionPeriod,
)
from office365.entity import Entity


class RetentionLabel(Entity):
    """
    Represents how organizations, for compliance and governance purposes, can manage their data at an item
    level (email or document), including whether and for how long to retain or delete the item.

     Organizations can use retention labels for different types of content that require different retention settings.
     For example, they can apply a retention label to tax forms and supporting documents to retain them for
     the period required by law.

     Organizations can configure retention labels with the retention periods and actions based on factors such
     as the date last modified or created. They can also start different retention periods by specifying an event
     that can trigger retention when the event occurs.

     For more information on how retention labels work, when to use them, and how Microsoft Purview supports
     retention labels to let you configure retention and deletion settings, see Learn about retention policies and
     retention labels.
    """

    @property
    def created_by(self) -> IdentitySet:
        """Represents the user who created the retentionLabel."""
        return self.properties.get("createdBy", IdentitySet())

    @property
    def retention_duration(self) -> RetentionDuration:
        """Specifies the number of days to retain the content."""
        return self.properties.get("retentionDuration", RetentionDuration())

    @property
    def behavior_during_retention_period(self) -> BehaviorDuringRetentionPeriod:
        """Specifies how the behavior of a document with this label should be during the retention period."""
        return self.properties.get(
            "behaviorDuringRetentionPeriod", BehaviorDuringRetentionPeriod.none
        )

    @property
    def retention_trigger(self) -> RetentionTrigger:
        """Specifies whether the retention duration is calculated from the content creation date, labeled date,
        or last modification date."""
        return self.properties.get("retentionTrigger", RetentionTrigger.none)

    @property
    def description_for_users(self) -> Optional[str]:
        """Provides the label information for the user. Optional."""
        return self.properties.get("descriptionForUsers", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.retentionLabel"
