from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class PermissionScope(ClientValue):
    """Represents the definition of a delegated permission.

    Delegated permissions can be requested by client applications needing an access token to the API which defined the
    permissions. Delegated permissions can be requested dynamically, using the scopes parameter in an authorization
    request to the Microsoft identity platform, or statically, through the requiredResourceAccess collection on the
    application object.

    Args:
        adminConsentDisplayName (str): The permission's title, intended to be read by an administrator granting the
        permission on behalf of all users.
        adminConsentDescription (str): A description of the delegated permissions, intended to be read by an
        administrator granting the permission on behalf of all users. This text appears in tenant-wide admin consent
        experiences.
        id (str): Unique delegated permission identifier inside the collection of delegated permissions defined
        for a resource application.
        isEnabled (str): When creating or updating a permission, this property must be set to true
        (which is the default). To delete a permission, this property must first be set to false. At that point, in
        a subsequent call, the permission may be removed.
        value (str): Specifies the value to include in the scp (scope) claim in access tokens.
    """

    adminConsentDescription: str | None = None
    adminConsentDisplayName: str | None = None
    id: str | None = None
    isEnabled: bool | None = None
    origin: str | None = None
    type: str | None = None
    userConsentDescription: str | None = None
    userConsentDisplayName: str | None = None
    value: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.PermissionScope"
