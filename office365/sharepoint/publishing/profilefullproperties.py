from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.person.identity import PersonIdentity
from office365.sharepoint.publishing.profiledatetime import ProfileDateTime


@dataclass
class ProfileFullProperties(ClientValue):
    AboutMe: Optional[str] = None
    AboutMeTruncated: Optional[str] = None
    Assistant: PersonIdentity = field(default_factory=lambda: PersonIdentity())
    BirthDate: ProfileDateTime = field(default_factory=lambda: ProfileDateTime())
    DepartmentName: Optional[str] = None
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
    Phone: Optional[str] = None
    PointPublishingPersonalSiteUrl: Optional[str] = None
    Responsibilities: Optional[str] = None
    Schools: Optional[str] = None
    Skills: Optional[str] = None
    SpsDepartment: Optional[str] = None
    SpsJobTitle: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfileFullProperties"
