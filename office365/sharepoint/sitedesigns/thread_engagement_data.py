from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ThreadEngagementData(ClientValue):
    commentCount: int | None = None
    reactionCount: int | None = None
    threadId: str | None = None
    viewerReaction: str | None = None
