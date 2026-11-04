from __future__ import annotations

from office365.runtime.types.value import value
from office365.security.labels.retention.duration import RetentionDuration


@value
class RetentionDurationInDays(RetentionDuration):
    """"""

    days: int | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.security.retentionDurationInDays"
