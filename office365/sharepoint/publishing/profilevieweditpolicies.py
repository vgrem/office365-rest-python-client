from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.profilepropertyvieweditpolicy import (
    ProfilePropertyViewEditPolicy,
)


class ProfileViewEditPolicies(ClientValue):
    def __init__(
        self,
        about_me: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        assistant: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        birthday: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        cell_phone: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        department: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        display_name: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        fax: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        hire_date: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        home_phone: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        interests: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        job_title: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        location: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        office: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        personal_site_url: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        picture_url: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        projects: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        responsibilities: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        schools: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        sip_address: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        skills: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        sps_department: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        sps_job_title: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        work_email: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
        work_phone: ProfilePropertyViewEditPolicy = ProfilePropertyViewEditPolicy(),
    ):
        self.AboutMe = about_me
        self.Assistant = assistant
        self.Birthday = birthday
        self.CellPhone = cell_phone
        self.Department = department
        self.DisplayName = display_name
        self.Fax = fax
        self.HireDate = hire_date
        self.HomePhone = home_phone
        self.Interests = interests
        self.JobTitle = job_title
        self.Location = location
        self.Office = office
        self.PersonalSiteUrl = personal_site_url
        self.PictureUrl = picture_url
        self.Projects = projects
        self.Responsibilities = responsibilities
        self.Schools = schools
        self.SipAddress = sip_address
        self.Skills = skills
        self.SpsDepartment = sps_department
        self.SpsJobTitle = sps_job_title
        self.WorkEmail = work_email
        self.WorkPhone = work_phone

    @property
    def entity_type_name(self):
        return "SP.Publishing.ProfileViewEditPolicies"
