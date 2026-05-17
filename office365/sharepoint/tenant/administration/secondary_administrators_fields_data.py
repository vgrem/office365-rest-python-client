from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from typing import Optional


class SecondaryAdministratorsFieldsData(ClientValue):
    def __init__(
        self,
        site_id=None,
        secondary_administrator_emails: Optional[StringCollection] = None,
        secondary_administrator_login_names: Optional[StringCollection] = None,
    ):
        """
        :type emails: List[str] or None
        :type names: List[str] or None
        :type site_id: str or None
        """
        super().__init__()
        self.siteId = site_id
        self.secondaryAdministratorEmails = secondary_administrator_emails
        self.secondaryAdministratorLoginNames = secondary_administrator_login_names

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SecondaryAdministratorsFieldsData"
