from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


class SPSyntexApplicationProperties(ClientValue):
    def __init__(
        self,
        application_id: UUID = None,
        application_name: str = None,
        applications: GuidCollection = GuidCollection(),
        app_only_permissions: StringCollection = StringCollection(),
        copilot_embedded_chat_hosts: StringCollection = StringCollection(),
        delegated_permissions: StringCollection = StringCollection(),
        override_tenant_sharing_capability: bool = None,
        override_tenant_sharing_capability_nullable: int = None,
        owning_application_id: UUID = None,
        owning_application_name: str = None,
        sharing_capability: int = None,
    ):
        self.ApplicationId = application_id
        self.ApplicationName = application_name
        self.Applications = applications
        self.AppOnlyPermissions = app_only_permissions
        self.CopilotEmbeddedChatHosts = copilot_embedded_chat_hosts
        self.DelegatedPermissions = delegated_permissions
        self.OverrideTenantSharingCapability = override_tenant_sharing_capability
        self.OverrideTenantSharingCapabilityNullable = override_tenant_sharing_capability_nullable
        self.OwningApplicationId = owning_application_id
        self.OwningApplicationName = owning_application_name
        self.SharingCapability = sharing_capability

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPSyntexApplicationProperties"
