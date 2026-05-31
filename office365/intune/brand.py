from __future__ import annotations

from office365.runtime.client_value import ClientValue


class IntuneBrand(ClientValue):
    contactITEmailAddress: str | None = None
    contactITName: str | None = None
    contactITNotes: str | None = None
    contactITPhoneNumber: str | None = None
    displayName: str | None = None
    onlineSupportSiteName: str | None = None
    onlineSupportSiteUrl: str | None = None
    privacyUrl: str | None = None
    showDisplayNameNextToLogo: bool | None = None
    showLogo: bool | None = None
    showNameNextToLogo: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IntuneBrand"
