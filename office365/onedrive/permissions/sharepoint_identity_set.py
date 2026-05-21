from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.permissions.identity import Identity
from office365.directory.permissions.identity_set import IdentitySet
from office365.onedrive.permissions.sharepoint_identity import SharePointIdentity


@dataclass
class SharePointIdentitySet(IdentitySet):
    """
    Represents a keyed collection of sharePointIdentity resources. This resource extends from the identitySet resource
    to provide the ability to expose SharePoint-specific information to the user.

    This resource is used to represent a set of identities associated with various events for an item,
    such as created by or last modified by.
    """

    group: Identity = field(default_factory=Identity)
    siteGroup: SharePointIdentity = field(default_factory=SharePointIdentity)
    siteUser: SharePointIdentity = field(default_factory=SharePointIdentity)
