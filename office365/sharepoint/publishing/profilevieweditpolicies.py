from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.profilepropertyvieweditpolicy import (
    ProfilePropertyViewEditPolicy,
)


@dataclass
class ProfileViewEditPolicies(ClientValue):
    AboutMe: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    Assistant: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    Birthday: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    CellPhone: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    Department: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    DisplayName: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    Fax: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    HireDate: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    HomePhone: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    Interests: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    JobTitle: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    Location: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    Office: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    PersonalSiteUrl: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    PictureUrl: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    Projects: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    Responsibilities: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    Schools: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    SipAddress: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    Skills: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    SpsDepartment: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    SpsJobTitle: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    WorkEmail: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)
    WorkPhone: ProfilePropertyViewEditPolicy = field(default_factory=ProfilePropertyViewEditPolicy)

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfileViewEditPolicies"
