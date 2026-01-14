from office365.runtime.client_value import ClientValue


class AsyncReadOptions(ClientValue):
    def __init__(
        self,
        include_direct_descendants_only: bool = None,
        include_extended_metadata: bool = None,
        include_permission: bool = None,
        include_security: bool = None,
        include_versions: bool = None,
        start_change_token: str = None,
    ):
        self.IncludeDirectDescendantsOnly = include_direct_descendants_only
        self.IncludeExtendedMetadata = include_extended_metadata
        self.IncludePermission = include_permission
        self.IncludeSecurity = include_security
        self.IncludeVersions = include_versions
        self.StartChangeToken = start_change_token
