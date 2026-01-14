from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.person.identity import PersonIdentity
from office365.sharepoint.publishing.profiledatetime import ProfileDateTime


class ProfileFullProperties(ClientValue):
    def __init__(
        self,
        about_me: str = None,
        about_me_truncated: str = None,
        assistant: PersonIdentity = PersonIdentity(),
        birth_date: ProfileDateTime = ProfileDateTime(),
        department_name: str = None,
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
        phone: str = None,
        point_publishing_personal_site_url: str = None,
        responsibilities: str = None,
        schools: str = None,
        skills: str = None,
        sps_department: str = None,
        sps_job_title: str = None,
    ):
        self.AboutMe = about_me
        self.AboutMeTruncated = about_me_truncated
        self.Assistant = assistant
        self.BirthDate = birth_date
        self.DepartmentName = department_name
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
        self.Phone = phone
        self.PointPublishingPersonalSiteUrl = point_publishing_personal_site_url
        self.Responsibilities = responsibilities
        self.Schools = schools
        self.Skills = skills
        self.SpsDepartment = sps_department
        self.SpsJobTitle = sps_job_title

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfileFullProperties"
