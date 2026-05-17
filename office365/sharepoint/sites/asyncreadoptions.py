from office365.runtime.client_value import ClientValue
from typing import Optional


class AsyncReadOptions(ClientValue):
    def __init__(
        self,
        include_direct_descendants_only: Optional[bool] = None,
        include_extended_metadata: Optional[bool] = None,
        include_permission: Optional[bool] = None,
        include_security: Optional[bool] = None,
        include_versions: Optional[bool] = None,
        start_change_token: Optional[str] = None,
    ):
        self.IncludeDirectDescendantsOnly = include_direct_descendants_only
        self.IncludeExtendedMetadata = include_extended_metadata
        self.IncludePermission = include_permission
        self.IncludeSecurity = include_security
        self.IncludeVersions = include_versions
        self.StartChangeToken = start_change_token
