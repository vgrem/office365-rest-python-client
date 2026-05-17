from typing import Optional

from office365.runtime.client_value import ClientValue


class SharingInformationRequest(ClientValue):
    def __init__(
        self,
        client_supported_features: Optional[str] = None,
        max_link_members_to_return: Optional[int] = None,
        max_principals_to_return: Optional[int] = None,
        populate_inherited_links: Optional[bool] = None,
    ):
        self.clientSupportedFeatures = client_supported_features
        self.maxLinkMembersToReturn = max_link_members_to_return
        self.maxPrincipalsToReturn = max_principals_to_return
        self.populateInheritedLinks = populate_inherited_links

    "Represents the optional Request Object for GetSharingInformation."

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingInformationRequest"
