from __future__ import annotations

from office365.runtime.client_value import ClientValue


class NewsDistributionSettings(ClientValue):
    communityId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.NewsDistributionSettings"
