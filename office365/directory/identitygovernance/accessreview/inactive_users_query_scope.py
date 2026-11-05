from __future__ import annotations

from datetime import timedelta

from office365.runtime.client_value import ClientValue


class AccessReviewInactiveUsersQueryScope(ClientValue):
    inactiveDuration: timedelta | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInactiveUsersQueryScope"
