from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.link_info import LinkInfo
from office365.sharepoint.sharing.mainaccessinformation import MainAccessInformation
from office365.sharepoint.utilities.principal_info import PrincipalInfo


@dataclass
class PermissionCollection(ClientValue):
    """
    This class is returned when Microsoft.SharePoint.Client.Sharing.SecurableObjectExtensions.GetSharingInformation
    is called with the optional expand on permissionsInformation property. It contains a collection of LinkInfo and
    PrincipalInfo objects of users/groups that have access to the list item and also the site administrators who have
    implicit access.

    :param bool has_inherited_links:
    :param list[LinkInfo] links: The List of tokenized sharing links with their LinkInfo objects.
    :param list[PrincipalInfo] principals: The List of Principals with their roles on this list item.
    :param list[PrincipalInfo] site_admins: The List of Principals who are Site Admins. This property is returned
        only if the caller is an Auditor.
    :param int total_number_of_principals:
    """
    appConsentPrincipals: ClientValueCollection[PrincipalInfo] = field(
        default_factory=lambda: ClientValueCollection(PrincipalInfo)
    )
    hasInheritedLinks: bool | None = None
    links: ClientValueCollection[LinkInfo] = field(
        default_factory=lambda: ClientValueCollection(LinkInfo)
    )
    principals: ClientValueCollection[PrincipalInfo] = field(
        default_factory=lambda: ClientValueCollection(PrincipalInfo)
    )
    siteAdmins: ClientValueCollection[PrincipalInfo] = field(
        default_factory=lambda: ClientValueCollection(PrincipalInfo)
    )
    totalNumberOfPrincipals: int | None = None
    mainAccess: MainAccessInformation = field(default_factory=MainAccessInformation)

    @property
    def entity_type_name(self):
        return "SP.Sharing.PermissionCollection"
