from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SecondaryAdministratorsFieldsData(ClientValue):
    def __init__(
        self,
        site_id=None,
        emails=None,
        names=None,
        secondary_administrator_emails: StringCollection = None,
        secondary_administrator_login_names: StringCollection = None,
    ):
        """
        :type emails: List[str] or None
        :type names: List[str] or None
        :type site_id: str or None
        """
        super().__init__()
        self.secondaryAdministratorEmails = StringCollection(emails)
        self.secondaryAdministratorLoginNames = StringCollection(names)
        self.siteId = site_id
        self.secondaryAdministratorEmails = secondary_administrator_emails
        self.secondaryAdministratorLoginNames = secondary_administrator_login_names

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SecondaryAdministratorsFieldsData"
