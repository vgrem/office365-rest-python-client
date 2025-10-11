from office365.runtime.client_value import ClientValue


class DisableGroupify(ClientValue):
    """ """

    def __init__(self, is_read_only: bool = None, value: bool = None) -> None:
        self.IsReadOnly = is_read_only
        self.Value = value

    def __repr__(self):
        return f"(IsReadOnly={self.IsReadOnly}, Value={self.Value})"

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.DisableGroupify"


class EnableAutoNewsDigest(ClientValue):
    """ """

    def __init__(self, is_read_only: bool = None, value: bool = None) -> None:
        self.IsReadOnly = is_read_only
        self.Value = value

    def __repr__(self):
        return f"(IsReadOnly={self.IsReadOnly}, Value={self.Value})"

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.EnableAutoNewsDigest"


class DisableSelfServiceSiteCreation(ClientValue):
    """ """

    def __init__(self, is_read_only: bool = None, value: bool = None) -> None:
        self.IsReadOnly = is_read_only
        self.Value = value

    def __repr__(self):
        return f"(IsReadOnly={self.IsReadOnly}, Value={self.Value})"

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.DisableSelfServiceSiteCreation"


class AutoQuotaEnabled(ClientValue):
    """Automatic quota management type"""

    def __init__(self, is_read_only=None, value=None):
        self.IsReadOnly = is_read_only
        self.Value = value

    def __repr__(self):
        return f"(IsReadOnly={self.IsReadOnly}, Value={self.Value})"

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.AutoQuotaEnabled"
