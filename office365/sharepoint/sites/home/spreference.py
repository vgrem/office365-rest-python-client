from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPHSiteReference(ClientValue):
    LogoUrl: str | None = None
    Title: str | None = None
    Url: str | None = None

    @property
    def entity_type_name(self):
        return "SP.SPHSiteReference"
