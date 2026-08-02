from __future__ import annotations

from office365.directory.security.labels.retention.duration import RetentionDuration


class RetentionDurationInDays(RetentionDuration):
    """"""

    days: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.security.retentionDurationInDays"
