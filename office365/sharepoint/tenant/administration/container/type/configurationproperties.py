from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


class SPContainerTypeConfigurationProperties(ClientValue):
    def __init__(
        self,
        anonymous_link_expiration_in_days: int = None,
        application_redirect_url: str = None,
        classification: int = None,
        container_type_id: UUID = None,
        container_type_name: str = None,
        copilot_embedded_chat_hosts: StringCollection = StringCollection(),
        is_discoverablility_disabled: int = None,
        is_move_disabled: int = None,
        is_rename_disabled: int = None,
        is_sharing_restricted: int = None,
        override_tenant_who_can_share_anonymous_allow_list: int = None,
        override_tenant_who_can_share_authenticated_guest_allow_list: int = None,
        owning_app_id: UUID = None,
        who_can_share_anonymous_allow_list: GuidCollection = GuidCollection(),
        who_can_share_authenticated_guest_allow_list: GuidCollection = GuidCollection(),
    ):
        self.AnonymousLinkExpirationInDays = anonymous_link_expiration_in_days
        self.ApplicationRedirectUrl = application_redirect_url
        self.Classification = classification
        self.ContainerTypeId = container_type_id
        self.ContainerTypeName = container_type_name
        self.CopilotEmbeddedChatHosts = copilot_embedded_chat_hosts
        self.IsDiscoverablilityDisabled = is_discoverablility_disabled
        self.IsMoveDisabled = is_move_disabled
        self.IsRenameDisabled = is_rename_disabled
        self.IsSharingRestricted = is_sharing_restricted
        self.OverrideTenantWhoCanShareAnonymousAllowList = override_tenant_who_can_share_anonymous_allow_list
        self.OverrideTenantWhoCanShareAuthenticatedGuestAllowList = (
            override_tenant_who_can_share_authenticated_guest_allow_list
        )
        self.OwningAppId = owning_app_id
        self.WhoCanShareAnonymousAllowList = who_can_share_anonymous_allow_list
        self.WhoCanShareAuthenticatedGuestAllowList = who_can_share_authenticated_guest_allow_list

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerTypeConfigurationProperties"
