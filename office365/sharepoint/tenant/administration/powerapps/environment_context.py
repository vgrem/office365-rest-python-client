from office365.runtime.client_value import ClientValue


class PowerAppsEnvironmentContext(ClientValue):

    def __init__(
        self,
        dataverse_instance_url=None,
        display_name=None,
        is_test_environment=None,
        last_get_environment_error=None,
        name=None,
        updated_utc=None,
    ):
        self.DataverseInstanceUrl = dataverse_instance_url
        self.DisplayName = display_name
        self.IsTestEnvironment = is_test_environment
        self.LastGetEnvironmentError = last_get_environment_error
        self.Name = name
        self.UpdatedUTC = updated_utc

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.PowerAppsEnvironmentContext"
