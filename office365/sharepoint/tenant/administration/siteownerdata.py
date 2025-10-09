from office365.runtime.client_value import ClientValue


class SiteOwnerData(ClientValue):

    def __init__(
        self,
        department: str = None,
        job_title: str = None,
        preferred_language: str = None,
        user_principal_name: str = None,
    ):
        self.department = department
        self.jobTitle = job_title
        self.preferredLanguage = preferred_language
        self.userPrincipalName = user_principal_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.SiteOwnerData"
