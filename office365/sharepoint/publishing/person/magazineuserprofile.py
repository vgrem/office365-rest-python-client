from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.datetimecustomproperty import (
    DateTimeCustomProperty,
)
from office365.sharepoint.publishing.person.core import PersonCore
from office365.sharepoint.publishing.person.customproperty import PersonCustomProperty
from office365.sharepoint.publishing.profiledatetime import ProfileDateTime


class PersonMagazineUserProfile(ClientValue):

    def __init__(
        self,
        aad_object_id: str = None,
        about_me: str = None,
        about_me_truncated: str = None,
        assistant: PersonCore = PersonCore(),
        birth_date: ProfileDateTime = ProfileDateTime(),
        birthday: str = None,
        date_time_custom_properties: ClientValueCollection[
            DateTimeCustomProperty
        ] = ClientValueCollection(DateTimeCustomProperty),
        department_name: str = None,
        display_name: str = None,
        email: str = None,
        fax: str = None,
        has_edit_permission: bool = None,
        hire_date: ProfileDateTime = ProfileDateTime(),
        home_phone: str = None,
        interest: str = None,
        lync: str = None,
        mobile_phone: str = None,
        office: str = None,
        office_location: str = None,
        one_drive_url: str = None,
        past_projects: str = None,
        person_type_custom_properties: ClientValueCollection[
            PersonCustomProperty
        ] = ClientValueCollection(PersonCustomProperty),
        phone: str = None,
        picture_url: str = None,
        point_publishing_personal_site_url: str = None,
        responsibilities: str = None,
        schools: str = None,
        skills: str = None,
        sps_department: str = None,
        sps_job_title: str = None,
        string_custom_properties: dict = None,
        title: str = None,
        user_name: str = None,
    ):
        self.AadObjectId = aad_object_id
        self.AboutMe = about_me
        self.AboutMeTruncated = about_me_truncated
        self.Assistant = assistant
        self.BirthDate = birth_date
        self.Birthday = birthday
        self.DateTimeCustomProperties = date_time_custom_properties
        self.DepartmentName = department_name
        self.DisplayName = display_name
        self.Email = email
        self.Fax = fax
        self.HasEditPermission = has_edit_permission
        self.HireDate = hire_date
        self.HomePhone = home_phone
        self.Interest = interest
        self.Lync = lync
        self.MobilePhone = mobile_phone
        self.Office = office
        self.OfficeLocation = office_location
        self.OneDriveUrl = one_drive_url
        self.PastProjects = past_projects
        self.PersonTypeCustomProperties = person_type_custom_properties
        self.Phone = phone
        self.PictureUrl = picture_url
        self.PointPublishingPersonalSiteUrl = point_publishing_personal_site_url
        self.Responsibilities = responsibilities
        self.Schools = schools
        self.Skills = skills
        self.SpsDepartment = sps_department
        self.SpsJobTitle = sps_job_title
        self.StringCustomProperties = string_custom_properties
        self.Title = title
        self.UserName = user_name

    @property
    def entity_type_name(self):
        return "SP.Publishing.PersonMagazineUserProfile"
