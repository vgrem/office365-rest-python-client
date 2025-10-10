from office365.runtime.client_value import ClientValue


class SiteCreationProperties(ClientValue):

    def __init__(
        self,
        title=None,
        url=None,
        owner=None,
        owner_name=None,
        template=None,
        site_uni_name=None,
        compatibility_level: int = None,
        lcid: str = None,
        time_zone_id: int = None,
        enable_agreements_solution: bool = None,
        storage_maximum_level: int = None,
        storage_warning_level: int = None,
        user_code_maximum_level: float = None,
        user_code_warning_level: float = None,
    ):
        """Sets the initial properties for a new site when it is created.

        :param str owner: Gets or sets the login name of the owner of the new site
        :param str url: Gets or sets the new site’s URL.
        :param str template: Gets or sets the web template name of the new site.
        :param str site_uni_name:
        """
        super().__init__()
        self.Url = url
        self.Owner = owner
        self.OwnerName = owner_name
        self.Title = title
        self.Template = template
        self.SiteUniName = site_uni_name
        self.CompatibilityLevel = compatibility_level
        self.Lcid = lcid
        self.TimeZoneId = time_zone_id
        self.EnableAgreementsSolution = enable_agreements_solution
        self.StorageMaximumLevel = storage_maximum_level
        self.StorageWarningLevel = storage_warning_level
        self.UserCodeMaximumLevel = user_code_maximum_level
        self.UserCodeWarningLevel = user_code_warning_level

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteCreationProperties"
