from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection
from typing import Optional


class SPSyntexApplicationProperties(ClientValue):
    def __init__(
        self,
        application_id: Optional[UUID] = None,
        application_name: Optional[str] = None,
        applications: GuidCollection = GuidCollection(),
        app_only_permissions: StringCollection = StringCollection(),
        copilot_embedded_chat_hosts: StringCollection = StringCollection(),
        delegated_permissions: StringCollection = StringCollection(),
        override_tenant_sharing_capability: Optional[bool] = None,
        override_tenant_sharing_capability_nullable: Optional[int] = None,
        owning_application_id: Optional[UUID] = None,
        owning_application_name: Optional[str] = None,
        sharing_capability: Optional[int] = None,
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
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPSyntexApplicationProperties"
