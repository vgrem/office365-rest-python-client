from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.profilepropertyvieweditpolicy import (
    ProfilePropertyViewEditPolicy,
)


@dataclass
class ProfileViewEditPolicies(ClientValue):
    AboutMe: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    Assistant: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    Birthday: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    CellPhone: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    Department: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    DisplayName: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    Fax: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    HireDate: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    HomePhone: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    Interests: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    JobTitle: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    Location: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    Office: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    PersonalSiteUrl: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    PictureUrl: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    Projects: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    Responsibilities: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    Schools: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    SipAddress: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    Skills: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    SpsDepartment: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    SpsJobTitle: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    WorkEmail: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())
    WorkPhone: ProfilePropertyViewEditPolicy = field(default_factory=lambda: ProfilePropertyViewEditPolicy())

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfileViewEditPolicies"
