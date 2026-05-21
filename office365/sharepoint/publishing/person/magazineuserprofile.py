from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.datetimecustomproperty import (
    DateTimeCustomProperty,
)
from office365.sharepoint.publishing.person.core import PersonCore
from office365.sharepoint.publishing.person.customproperty import PersonCustomProperty
from office365.sharepoint.publishing.profiledatetime import ProfileDateTime


@dataclass
class PersonMagazineUserProfile(ClientValue):
    AadObjectId: Optional[str] = None
    AboutMe: Optional[str] = None
    AboutMeTruncated: Optional[str] = None
    Assistant: PersonCore = field(default_factory=lambda: PersonCore())
    BirthDate: ProfileDateTime = field(default_factory=lambda: ProfileDateTime())
    Birthday: Optional[str] = None
    DateTimeCustomProperties: ClientValueCollection[DateTimeCustomProperty] = field(
        default_factory=lambda: ClientValueCollection(DateTimeCustomProperty)
    )
    DepartmentName: Optional[str] = None
    DisplayName: Optional[str] = None
    Email: Optional[str] = None
    Fax: Optional[str] = None
    HasEditPermission: Optional[bool] = None
    HireDate: ProfileDateTime = field(default_factory=lambda: ProfileDateTime())
    HomePhone: Optional[str] = None
    Interest: Optional[str] = None
    Lync: Optional[str] = None
    MobilePhone: Optional[str] = None
    Office: Optional[str] = None
    OfficeLocation: Optional[str] = None
    OneDriveUrl: Optional[str] = None
    PastProjects: Optional[str] = None
    PersonTypeCustomProperties: ClientValueCollection[PersonCustomProperty] = field(
        default_factory=lambda: ClientValueCollection(PersonCustomProperty)
    )
    Phone: Optional[str] = None
    PictureUrl: Optional[str] = None
    PointPublishingPersonalSiteUrl: Optional[str] = None
    Responsibilities: Optional[str] = None
    Schools: Optional[str] = None
    Skills: Optional[str] = None
    SpsDepartment: Optional[str] = None
    SpsJobTitle: Optional[str] = None
    StringCustomProperties: dict = field(default_factory=dict)
    Title: Optional[str] = None
    UserName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PersonMagazineUserProfile"
