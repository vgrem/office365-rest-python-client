from office365.intune.devices.management.virtualendpoint.cloudpcs.userrolescopetaginfo import CloudPcUserRoleScopeTagInfo
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


class CloudPcAuditActor(ClientValue):
    def __init__(
        self,
        application_display_name: str = None,
        application_id: str = None,
        ip_address: str = None,
        remote_tenant_id: str = None,
        remote_user_id: str = None,
        service_principal_name: str = None,
        user_id: str = None,
        user_permissions: StringCollection = None,
        user_principal_name: str = None,
        user_role_scope_tags: ClientValueCollection[CloudPcUserRoleScopeTagInfo] = ClientValueCollection(
            CloudPcUserRoleScopeTagInfo
        ),
    ):
        self.applicationDisplayName = application_display_name
        self.applicationId = application_id
        self.ipAddress = ip_address
        self.remoteTenantId = remote_tenant_id
        self.remoteUserId = remote_user_id
        self.servicePrincipalName = service_principal_name
        self.userId = user_id
        self.userPermissions = user_permissions
        self.userPrincipalName = user_principal_name
        self.userRoleScopeTags = user_role_scope_tags

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcAuditActor"
