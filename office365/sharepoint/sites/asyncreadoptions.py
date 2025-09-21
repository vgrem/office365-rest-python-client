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
        self.include_direct_descendants_only = include_direct_descendants_only
        self.include_extended_metadata = include_extended_metadata
        self.include_permission = include_permission
        self.include_security = include_security
        self.include_versions = include_versions
        self.start_change_token = start_change_token
