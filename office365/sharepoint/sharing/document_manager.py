from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions.roles.definitions.definition import RoleDefinition
from office365.sharepoint.portal.userprofiles.sharedwithme.view_item_removal_result import (
    SharedWithMeViewItemRemovalResult,
)
from office365.sharepoint.sharing.role_type import RoleType
from office365.sharepoint.sharing.user_role_assignment import UserRoleAssignment
from office365.sharepoint.sharing.user_sharing_result import UserSharingResult

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class DocumentSharingManager(Entity):
    """Specifies document sharing related methods."""

    @staticmethod
    def get_role_definition(context: ClientContext, role: RoleType):
        """This method returns a role definition in the current web that is associated with a given Role
        (section 3.2.5.188) value.

        Args:
            context (office365.sharepoint.client_context.ClientContext):
            role (int): A Role value for which to obtain the associated role definition object.
        """
        return_type = RoleDefinition(context)
        context.web.role_definitions.add_child(return_type)
        binding_type = DocumentSharingManager(context)
        qry = ServiceOperationQuery(
            binding_type,
            "GetRoleDefinition",
            [role.value],
            None,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def remove_items_from_shared_with_me_view(
        context: ClientContext, item_urls: List[str]
    ) -> ClientResult[ClientValueCollection[SharedWithMeViewItemRemovalResult]]:
        """Removes an item so that it no longer shows in the current user's 'Shared With Me' view. However, this
        does not remove the user's actual permissions to the item. Up to 200 items can be provided in a single call.
        Returns a list of results indicating whether the items were successfully removed. The length of this array
        will match the length of the itemUrls array that was provided.

        Args:
            context (office365.sharepoint.client_context.ClientContext):
            item_urls (list[str]): A list of absolute URLs of the items to be removed from the view. These items might belong to any site or site collection in the tenant.
        """
        return_type = ClientResult(context, ClientValueCollection(SharedWithMeViewItemRemovalResult))
        binding_type = DocumentSharingManager(context)
        qry = ServiceOperationQuery(
            binding_type,
            "RemoveItemsFromSharedWithMeView",
            [item_urls],
            None,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def update_document_sharing_info(
        context: ClientContext,
        resource_address: str,
        user_role_assignments: List[UserRoleAssignment],
        validate_existing_permissions: Optional[bool] = None,
        additive_mode: Optional[bool] = None,
        send_server_managed_notification=None,
        custom_message=None,
        include_anonymous_links_in_notification=None,
        propagate_acl=None,
        return_type=None,
    ):
        """This method allows a caller with the 'ManagePermission' permission to update sharing information about a
        document to enable document sharing with a set of users. It returns an array of
        UserSharingResult (section 3.2.5.190) elements where each element contains the sharing status for each user.

        Args:
            context (office365.sharepoint.client_context.ClientContext):
            resource_address (str): A URL that points to a securable object, which can be a document, folder or the root folder of a document library.
            user_role_assignments (list[UserRoleAssignment]): An array of recipients and assigned roles on the securable object pointed to by the resourceAddress parameter.
            validate_existing_permissions (bool): A Boolean flag indicating how to honor a requested permission for a user. If this value is "true", the protocol server will not grant the requested permission if a user already has sufficient permissions, and if this value is "false", the protocol server will grant the requested permission whether or not a user already has the same or more permissions. This parameter is applicable only when the parameter additiveMode is set to true.
            additive_mode (bool): A Boolean flag indicating whether the permission setting uses the additive or strict mode. If this value is "true", the permission setting uses the additive mode, which means that the specified permission will be added to the user's current list of permissions if it is not there already, and if this value is "false", the permission setting uses the strict mode, which means that the specified permission will replace the user's current permissions.
            send_server_managed_notification (bool): A Boolean flag to indicate whether or not to generate an email notification to each recipient in the "userRoleAssignments" array after the document update is completed successfully. If this value is "true", the protocol server will send an email notification if an email server is configured, and if the value is "false", no email notification will be sent.
            custom_message (str): A custom message to be included in the email notification.
            include_anonymous_links_in_notification (bool): A Boolean flag that indicates whether or not to include anonymous access links in the email notification to each recipient in the userRoleAssignments array after the document update is completed successfully. If the value is "true", the protocol server will include an anonymous access link in the email notification, and if the value is "false", no link will be included.
            propagate_acl (bool): A flag to determine if permissions SHOULD be pushed to items with unique permission.
            return_type (ClientResult):
        """
        if return_type is None:
            return_type = ClientResult(context, ClientValueCollection(UserSharingResult))
        payload = {
            "resourceAddress": resource_address,
            "userRoleAssignments": user_role_assignments,
            "validateExistingPermissions": validate_existing_permissions,
            "additiveMode": additive_mode,
            "sendServerManagedNotification": send_server_managed_notification,
            "customMessage": custom_message,
            "includeAnonymousLinksInNotification": include_anonymous_links_in_notification,
            "propagateAcl": propagate_acl,
        }
        binding_type = DocumentSharingManager(context)
        qry = ServiceOperationQuery(
            binding_type,
            "UpdateDocumentSharingInfo",
            None,
            payload,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.Sharing.DocumentSharingManager"
