from office365.delta_collection import DeltaCollection
from office365.directory.permissions.grants.oauth2 import OAuth2PermissionGrant


class OAuth2PermissionGrantCollection(DeltaCollection[OAuth2PermissionGrant]):
    """DirectoryObject's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, OAuth2PermissionGrant, resource_path)
