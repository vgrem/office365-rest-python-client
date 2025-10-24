from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from typing_extensions import Self

from office365.admin.admin import Admin
from office365.azure_env import AzureEnvironment
from office365.booking.solutions.root import SolutionsRoot
from office365.communications.cloud_communications import CloudCommunications
from office365.copilot.root import CopilotRoot
from office365.delta_collection import DeltaCollection
from office365.directory.applications.collection import ApplicationCollection
from office365.directory.applications.template import ApplicationTemplate
from office365.directory.audit.log_root import AuditLogRoot
from office365.directory.authentication.methods.configuration import (
    AuthenticationMethodConfiguration,
)
from office365.directory.certificates.auth_configuration import (
    CertificateBasedAuthConfiguration,
)
from office365.directory.directory import Directory
from office365.directory.domains.domain import Domain
from office365.directory.extensions.schema import SchemaExtension
from office365.directory.groups.collection import GroupCollection
from office365.directory.groups.lifecycle_policy import GroupLifecyclePolicy
from office365.directory.groups.setting_template import GroupSettingTemplate
from office365.directory.identities.container import IdentityContainer
from office365.directory.identities.provider import IdentityProvider
from office365.directory.identitygovernance.governance import IdentityGovernance
from office365.directory.internal.paths.me import MePath
from office365.directory.invitations.collection import InvitationCollection
from office365.directory.licenses.subscribed_sku import SubscribedSku
from office365.directory.objects.collection import DirectoryObjectCollection
from office365.directory.permissions.grants.oauth2 import OAuth2PermissionGrant
from office365.directory.permissions.grants.resource_specific import (
    ResourceSpecificPermissionGrant,
)
from office365.directory.policies.root import PolicyRoot
from office365.directory.protection.information import InformationProtection
from office365.directory.protection.root import IdentityProtectionRoot
from office365.directory.rolemanagement.management import RoleManagement
from office365.directory.rolemanagement.role import DirectoryRole
from office365.directory.security.security import Security
from office365.directory.serviceprincipals.collection import ServicePrincipalCollection
from office365.directory.tenantinformation.relationship import TenantRelationship
from office365.directory.users.collection import UserCollection
from office365.directory.users.user import User
from office365.education.root import EducationRoot
from office365.entity_collection import EntityCollection
from office365.graph_request import GraphRequest
from office365.intune.devices.app_management import DeviceAppManagement
from office365.intune.devices.collection import DeviceCollection
from office365.intune.devices.management.management import DeviceManagement
from office365.intune.organizations.contact import OrgContact
from office365.intune.organizations.organization import Organization
from office365.intune.print.print import Print
from office365.onedrive.drives.drive import Drive
from office365.onedrive.shares.collection import SharesCollection
from office365.onedrive.sites.sites_with_root import SitesWithRoot
from office365.onedrive.storage.storage import Storage
from office365.outlook.calendar.place import Place
from office365.outlook.calendar.rooms.list import RoomList
from office365.planner.planner import Planner
from office365.reports.root import ReportRoot
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.v4.batch_request import ODataV4BatchRequest
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.delete_entity import DeleteEntityQuery
from office365.runtime.queries.update_entity import UpdateEntityQuery
from office365.search.entity import SearchEntity
from office365.search.external.connection import ExternalConnection
from office365.search.external.external import External
from office365.subscriptions.collection import SubscriptionCollection
from office365.teams.apps.catalog import AppCatalogs
from office365.teams.chats.collection import ChatCollection
from office365.teams.collection import TeamCollection
from office365.teams.template import TeamsTemplate
from office365.teams.viva.employee_experience import EmployeeExperience
from office365.teams.work import Teamwork

if TYPE_CHECKING:
    from office365.directory.groups.setting import GroupSetting


class GraphClient(ClientRuntimeContext):
    """Microsoft Graph API client"""

    def __init__(
        self,
        token_callback: Callable[[], Dict[str, str]] = None,
        tenant: str = None,
        scopes: List[str] = None,
        token_cache: Any = None,
        environment: AzureEnvironment = AzureEnvironment.Global,
    ):
        """
        Initialize Microsoft Graph client

        Args:
            token_callback: Optional token callback function
            tenant: Tenant ID or domain name
            scopes: List of permission scopes
            token_cache: Token cache implementation. Refer
                https://msal-python.readthedocs.io/en/latest/#msal.SerializableTokenCache
            environment: Azure environment (default: AzureEnvironment.Global)
        """

        super().__init__()
        self._pending_request = None
        self._token_callback = token_callback
        self._tenant = tenant
        self._token_cache = token_cache
        self._environment = environment
        self._scopes = scopes
        self._directory: Optional[Directory] = None

    def with_certificate(self, client_id: str, thumbprint: str, private_key: str) -> Self:
        """
        Initialize with client certificate authentication

        Args:
            client_id: Application client ID
            thumbprint: Certificate thumbprint
            private_key: Private key content

        Returns:
            self: Supports method chaining
        """
        self.pending_request().with_certificate(client_id, thumbprint, private_key)
        return self

    def with_client_secret(self, client_id: str, client_secret: str) -> Self:
        """
        Initialize with client secret authentication

        Args:
            client_id: Application client ID
            client_secret: Client secret value

        Returns:
            self: Supports method chaining
        """
        self.pending_request().with_client_secret(client_id, client_secret)
        return self

    def with_token_interactive(self, client_id: str, username: Optional[str] = None) -> Self:
        """
        Initialize with interactive authentication flow

        Args:
            client_id: Application client ID
            username: Optional username for authentication
        """
        self.pending_request().with_token_interactive(client_id, username)
        return self

    def with_username_and_password(self, client_id: str, username: str, password: str) -> Self:
        """
        Initialize with username/password authentication

        Args:
            client_id: Application client ID
            username: User principal name
            password: User password
        """
        self.pending_request().with_username_and_password(client_id, username, password)
        return self

    def execute_batch(
        self,
        items_per_batch: int = 20,
        success_callback: Callable[[List[Any]], None] = None,
    ):
        """
        Execute batched requests

        Args:
            items_per_batch: Maximum items per batch (default: 20)
            success_callback: Optional callback for successful requests
        """
        batch_request = ODataV4BatchRequest(V4JsonFormat())
        batch_request.beforeExecute += self.pending_request().authenticate_request
        while self.has_pending_request:
            qry = self._get_next_query(items_per_batch)
            batch_request.execute_query(qry)
            if callable(success_callback):
                success_callback(qry.return_type)
        return self

    def pending_request(self) -> GraphRequest:
        """Get or create the pending request"""
        if self._pending_request is None:
            self._pending_request = GraphRequest(tenant=self._tenant, environment=self._environment)
            if callable(self._token_callback):
                self._pending_request.with_access_token(self._token_callback)
            self._pending_request.beforeExecute += self._build_specific_query
        return self._pending_request

    @property
    def service_root_url(self) -> str:
        """Get the Graph API service root URL"""
        return self.pending_request().service_root_url

    def _build_specific_query(self, request: RequestOptions) -> None:
        """Build Graph-specific HTTP request"""
        if isinstance(self.current_query, UpdateEntityQuery):
            request.method = HttpMethod.Patch
        elif isinstance(self.current_query, DeleteEntityQuery):
            request.method = HttpMethod.Delete

    @property
    def admin(self) -> Admin:
        """A container for administrator functionality for SharePoint and OneDrive."""
        return Admin(self, ResourcePath("admin"))

    @property
    def app_catalogs(self) -> AppCatalogs:
        """A container for apps from the Microsoft Teams app catalog."""
        return AppCatalogs(self, ResourcePath("appCatalogs"))

    @property
    def me(self) -> User:
        """The Me endpoint is provided as a shortcut for specifying the current user"""
        return User(self, MePath())

    @property
    def device_management(self) -> DeviceManagement:
        """Singleton entity that acts as a container for all device management functionality."""
        return DeviceManagement(self, ResourcePath("deviceManagement"))

    @property
    def device_app_management(self) -> DeviceAppManagement:
        """Singleton entity that acts as a container for all device and app management functionality."""
        return DeviceAppManagement(self, ResourcePath("deviceAppManagement"))

    @property
    def drives(self) -> EntityCollection[Drive]:
        """Get one drives"""
        return EntityCollection(self, Drive, ResourcePath("drives"))

    @property
    def users(self) -> UserCollection:
        """Users container"""
        return UserCollection(self, ResourcePath("users"))

    @property
    def domains(self) -> EntityCollection[Domain]:
        """Alias to domains"""
        return EntityCollection(self, Domain, ResourcePath("domains"))

    @property
    def groups(self) -> GroupCollection:
        """Get groups"""
        return GroupCollection(self, ResourcePath("groups"))

    @property
    def invitations(self) -> InvitationCollection:
        """Get invitations"""
        return InvitationCollection(self, ResourcePath("invitations"))

    @property
    def copilot(self) -> CopilotRoot:
        """"""
        return CopilotRoot(self, ResourcePath("copilot"))

    @property
    def identity_protection(self) -> IdentityProtectionRoot:
        """Identity Protection alias"""
        return IdentityProtectionRoot(self, ResourcePath("identityProtection"))

    @property
    def sites(self) -> SitesWithRoot:
        """Sites container"""
        return SitesWithRoot(self, ResourcePath("sites"))

    @property
    def shares(self) -> SharesCollection:
        """Shares container"""
        return SharesCollection(self, ResourcePath("shares"))

    @property
    def directory_objects(self) -> DirectoryObjectCollection:
        """Directory Objects container"""
        return DirectoryObjectCollection(self, ResourcePath("directoryObjects"))

    @property
    def devices(self) -> DeviceCollection:
        """Devices container"""
        return DeviceCollection(self, ResourcePath("devices"))

    @property
    def teams(self) -> TeamCollection:
        """Teams container"""
        return TeamCollection(self, ResourcePath("teams"))

    @property
    def chats(self) -> ChatCollection:
        """Chats container"""
        return ChatCollection(self, ResourcePath("chats"))

    @property
    def group_setting_templates(self) -> EntityCollection[GroupSettingTemplate]:
        """Group setting templates represent system-defined settings available to the tenant."""
        return EntityCollection(self, GroupSettingTemplate, ResourcePath("groupSettingTemplates"))

    @property
    def contacts(self) -> DeltaCollection[OrgContact]:
        """Get the list of organizational contacts for this organization."""
        return DeltaCollection(self, OrgContact, ResourcePath("contacts"))

    @property
    def directory(self) -> Directory:
        """Represents a deleted item in the directory"""
        if self._directory is None:
            self._directory = Directory(self, ResourcePath("directory"))
        return self._directory

    @property
    def directory_roles(self) -> DeltaCollection[DirectoryRole]:
        """Represents a directory roles in the directory"""
        return DeltaCollection(self, DirectoryRole, ResourcePath("directoryRoles"))

    @property
    def directory_role_templates(self):
        """Represents a directory role templates in the directory"""
        from office365.directory.rolemanagement.template import DirectoryRoleTemplate

        return EntityCollection(self, DirectoryRoleTemplate, ResourcePath("directoryRoleTemplates"))

    @property
    def identity_providers(self) -> EntityCollection[IdentityProvider]:
        """"""
        return EntityCollection(self, IdentityProvider, ResourcePath("identityProviders"))

    @property
    def identity(self) -> IdentityContainer:
        return IdentityContainer(self, ResourcePath("identity"))

    @property
    def application_templates(self) -> EntityCollection[ApplicationTemplate]:
        """Get the list of application templates in this organization."""
        return EntityCollection(self, ApplicationTemplate, ResourcePath("applicationTemplates"))

    @property
    def authentication_method_configurations(
        self,
    ) -> EntityCollection[AuthenticationMethodConfiguration]:
        """Get the list of application templates in this organization."""
        return EntityCollection(
            self,
            AuthenticationMethodConfiguration,
            ResourcePath("authenticationMethodConfigurations"),
        )

    @property
    def applications(self) -> ApplicationCollection:
        """Get the list of applications in this organization."""
        return ApplicationCollection(self, ResourcePath("applications"))

    @property
    def certificate_based_auth_configuration(
        self,
    ) -> EntityCollection[CertificateBasedAuthConfiguration]:
        """Get the list of applications in this organization."""
        return EntityCollection(
            self,
            CertificateBasedAuthConfiguration,
            ResourcePath("certificateBasedAuthConfiguration"),
        )

    @property
    def service_principals(self) -> ServicePrincipalCollection:
        """Retrieve a list of servicePrincipal objects."""
        return ServicePrincipalCollection(self, ResourcePath("servicePrincipals"))

    @property
    def organization(self) -> EntityCollection[Organization]:
        """"""
        return EntityCollection(self, Organization, ResourcePath("organization"))

    @property
    def subscribed_skus(self) -> EntityCollection[SubscribedSku]:
        """Get the list of commercial subscriptions that an organization has acquired"""
        return EntityCollection(self, SubscribedSku, ResourcePath("subscribedSkus"))

    @property
    def group_lifecycle_policies(self) -> EntityCollection[GroupLifecyclePolicy]:
        """A collection of lifecycle policies for a Microsoft 365 groups."""
        return EntityCollection(self, GroupLifecyclePolicy, ResourcePath("groupLifecyclePolicies"))

    @property
    def group_settings(self) -> GroupSetting:
        """Represents a directory roles in the directory"""
        from office365.directory.groups.setting import GroupSetting

        return GroupSetting(self, ResourcePath("groupSettings"))

    @property
    def communications(self) -> CloudCommunications:
        """Cloud communications API endpoint"""
        return CloudCommunications(self, ResourcePath("communications"))

    @property
    def identity_governance(self) -> IdentityGovernance:
        """The identity governance singleton"""
        return IdentityGovernance(self, ResourcePath("identityGovernance"))

    @property
    def information_protection(self) -> InformationProtection:
        """
        Exposes methods that you can use to get Microsoft Purview Information Protection labels and label policies.
        """
        return InformationProtection(self, ResourcePath("informationProtection"))

    @property
    def storage(self) -> Storage:
        """
        Facilitates the structures of fileStorageContainers.
        """
        return Storage(self, ResourcePath("storage"))

    @property
    def subscriptions(self) -> SubscriptionCollection:
        """
        Retrieve the properties and relationships of webhook subscriptions,
        based on the app ID, the user, and the user's role with a tenant.
        """
        return SubscriptionCollection(self, ResourcePath("subscriptions"))

    @property
    def connections(self) -> EntityCollection[ExternalConnection]:
        """Get a list of the externalConnection objects and their properties."""
        from office365.search.external.connection import ExternalConnection

        return EntityCollection(self, ExternalConnection, ResourcePath("connections"))

    @property
    def tenant_relationships(self) -> TenantRelationship:
        """Represent the various type of tenant relationships."""
        return TenantRelationship(self, ResourcePath("tenantRelationships"))

    @property
    def audit_logs(self) -> AuditLogRoot:
        """Gets the list of audit logs generated by Azure Active Directory."""
        return AuditLogRoot(self, ResourcePath("auditLogs"))

    @property
    def places(self) -> EntityCollection[Place]:
        """Gets all places in a tenant"""
        return EntityCollection(self, Place, ResourcePath("places"))

    @property
    def oauth2_permission_grants(self) -> DeltaCollection[OAuth2PermissionGrant]:
        """Permission grants container"""
        return DeltaCollection(self, OAuth2PermissionGrant, ResourcePath("oauth2PermissionGrants"))

    @property
    def room_lists(self) -> EntityCollection[RoomList]:
        """Gets all the room lists in a tenant"""
        return EntityCollection(
            self,
            RoomList,
            ResourcePath("microsoft.graph.roomlist", ResourcePath("places")),
        )

    @property
    def reports(self) -> ReportRoot:
        """Represents a container for Azure Active Directory (Azure AD) reporting resources."""
        return ReportRoot(self, ResourcePath("reports"))

    @property
    def role_management(self) -> RoleManagement:
        """Represents a Microsoft 365 role-based access control (RBAC) role management container"""
        return RoleManagement(self, ResourcePath("roleManagement"))

    @property
    def solutions(self) -> SolutionsRoot:
        return SolutionsRoot(self, ResourcePath("solutions"))

    @property
    def teams_templates(self) -> EntityCollection[TeamsTemplate]:
        """Get the list of teams templates."""
        return EntityCollection(self, TeamsTemplate, ResourcePath("teamsTemplates"))

    @property
    def planner(self) -> Planner:
        """
        The planner resource is the entry point for the Planner object model.
        It returns a singleton planner resource. It doesn't contain any usable properties.
        """
        return Planner(self, ResourcePath("planner"))

    @property
    def permission_grants(self) -> EntityCollection[ResourceSpecificPermissionGrant]:
        """List all resource-specific permission grants"""
        return EntityCollection(self, ResourceSpecificPermissionGrant, ResourcePath("permissionGrants"))

    @property
    def print(self) -> Print:
        """Used to manage printers and print jobs within Universal Print."""
        return Print(self, ResourcePath("print"))

    @property
    def search(self) -> SearchEntity:
        """The search endpoint is the entry point for Microsoft Search API to query data."""
        return SearchEntity(self, ResourcePath("search"))

    @property
    def employee_experience(self) -> EmployeeExperience:
        """An alias to EmployeeExperience"""
        return EmployeeExperience(self, ResourcePath("employeeExperience"))

    @property
    def education(self) -> EducationRoot:
        """
        The /education namespace exposes functionality that is specific to the education sector.
        """
        return EducationRoot(self, ResourcePath("education"))

    @property
    def policies(self) -> PolicyRoot:
        """Resource type exposing navigation properties for the policies singleton."""
        return PolicyRoot(self, ResourcePath("policies"))

    @property
    def external(self) -> External:
        """A logical container for external sources."""
        return External(self, ResourcePath("external"))

    @property
    def security(self) -> Security:
        """The security resource is the entry point for the Security object model.
        It returns a singleton security resource. It doesn't contain any usable properties.
        """
        return Security(self, ResourcePath("security"))

    @property
    def schema_extensions(self) -> EntityCollection[SchemaExtension]:
        """Get a list of schemaExtension objects in your tenant"""
        return EntityCollection(self, SchemaExtension, ResourcePath("schemaExtensions"))

    @property
    def teamwork(self) -> Teamwork:
        """A container for the range of Microsoft Teams functionalities that are available for the organization."""
        return Teamwork(self, ResourcePath("teamwork"))

    @property
    def tenant_name(self) -> str:
        """Tenant id or domain name"""
        return self._tenant
