from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteOwnerData(ClientValue):
    def __init__(
        self,
        department: Optional[str] = None,
        job_title: Optional[str] = None,
        preferred_language: Optional[str] = None,
        user_principal_name: Optional[str] = None,
    ):
        self.department = department
        self.jobTitle = job_title
        self.preferredLanguage = preferred_language
        self.userPrincipalName = user_principal_name

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.SiteOwnerData"
