from office365.runtime.client_value import ClientValue
from typing import Optional
from dataclasses import dataclass, field

class IntuneBrand(ClientValue):
    contactITEmailAddress: str | None = None
    contactITName: str | None = None
    contactITNotes: str | None = None
    contactITPhoneNumber: str | None = None
    darkBackgroundLogo: MimeContent = field(default_factory=MimeContent)
    displayName: str | None = None
    lightBackgroundLogo: MimeContent = field(default_factory=MimeContent)
    onlineSupportSiteName: str | None = None
    onlineSupportSiteUrl: str | None = None
    privacyUrl: str | None = None
    showDisplayNameNextToLogo: bool | None = None
    showLogo: bool | None = None
    showNameNextToLogo: bool | None = None
    themeColor: RgbColor = field(default_factory=RgbColor)
    'intuneBrand contains data which is used in customizing the appearance of the Company Portal applications as\n    well as the end user web portal.'

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.IntuneBrand'