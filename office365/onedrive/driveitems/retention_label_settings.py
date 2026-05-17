from __future__ import annotations

from office365.directory.security.labels.retention.behaviorduringretentionperiod import (
    BehaviorDuringRetentionPeriod,
)
from office365.runtime.client_value import ClientValue


class RetentionLabelSettings(ClientValue):
    """
    Groups all the compliance retention restrictions on the item into a single structure.
    """

    def __init__(
        self,
        behavior_during_retention_period: BehaviorDuringRetentionPeriod | None = None,
        is_content_update_allowed: bool | None = None,
        is_delete_allowed: bool | None = None,
        is_label_update_allowed: bool | None = None,
        is_metadata_update_allowed: bool | None = None,
        is_record_locked: bool | None = None,
    ):
        self.behaviorDuringRetentionPeriod = behavior_during_retention_period
        self.isContentUpdateAllowed = is_content_update_allowed
        self.isDeleteAllowed = is_delete_allowed
        self.isLabelUpdateAllowed = is_label_update_allowed
        self.isMetadataUpdateAllowed = is_metadata_update_allowed
        self.isRecordLocked = is_record_locked
