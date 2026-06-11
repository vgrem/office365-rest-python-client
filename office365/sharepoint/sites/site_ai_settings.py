from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class SiteAISettings(ClientValue):
    ErrorMessage: str | None = None
    IsRestrictedContentDiscoverabilityEnabled: bool | None = None
    IsSuccess: bool | None = None
    KnowledgeAgentEnabled: bool | None = None
    SiteId: UUID | None = None
