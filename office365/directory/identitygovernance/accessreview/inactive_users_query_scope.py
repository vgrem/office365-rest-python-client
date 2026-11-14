from __future__ import annotations

from datetime import timedelta

from office365.directory.identitygovernance.accessreview.query_scope import AccessReviewQueryScope


class AccessReviewInactiveUsersQueryScope(AccessReviewQueryScope):
    inactiveDuration: timedelta | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInactiveUsersQueryScope"
