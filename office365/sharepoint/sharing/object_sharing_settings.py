from __future__ import annotations

from typing import Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.sharing.object_sharing_information import (
    ObjectSharingInformation,
)
from office365.sharepoint.sharing.permission_information import (
    SharingPermissionInformation,
)
from office365.sharepoint.sharing.sharepoint_sharing_settings import (
    SharePointSharingSettings,
)


class ObjectSharingSettings(Entity):
    """This class contains the information necessary to read and change the sharing status of a SharePoint object.
    It also contains a reference to SharePoint specific settings denoted by "SharePointSettings".
    """

    @odata(name="WebUrl")
    @property
    def web_url(self) -> Optional[str]:
        """The URL pointing to the containing SP.Web object."""
        return self.properties.get("WebUrl", None)

    @odata(name="AccessRequestMode")
    @property
    def access_request_mode(self) -> Optional[bool]:
        """Boolean indicating whether the sharing context operates under the access request mode."""
        return self.properties.get("AccessRequestMode", None)

    @odata(name="BlockPeoplePickerAndSharing")
    @property
    def block_people_picker_and_sharing(self) -> Optional[bool]:
        """Boolean indicating whether the current user can use the People Picker to do any sharing."""
        return self.properties.get("BlockPeoplePickerAndSharing", None)

    @odata(name="CanCurrentUserManageOrganizationReadonlyLink")
    @property
    def can_current_user_manage_organization_readonly_link(self) -> Optional[bool]:
        """Boolean indicating whether the current user can create or disable an organization View link."""
        return self.properties.get("CanCurrentUserManageOrganizationReadonlyLink", None)

    @odata(name="CanCurrentUserManageOrganizationReadWriteLink")
    @property
    def can_current_user_manage_organization_read_write_link(self) -> Optional[bool]:
        """Boolean indicating whether the current user can create or disable an organization Edit link."""
        return self.properties.get("CanCurrentUserManageOrganizationReadWriteLink", None)

    @odata(name="CanCurrentUserManageReadonlyLink")
    @property
    def can_current_user_manage_readonly_link(self) -> Optional[bool]:
        """Boolean indicating whether the current user can create or disable an anonymous View link."""
        return self.properties.get("CanCurrentUserManageReadonlyLink", None)

    @odata(name="CanSendEmail")
    @property
    def can_send_email(self) -> Optional[bool]:
        """Boolean indicating whether email invitations can be sent."""
        return self.properties.get("CanSendEmail", None)

    @odata(name="CanSendLink")
    @property
    def can_send_link(self) -> Optional[bool]:
        """Boolean indicating whether the current user can make use of Share-By-Link."""
        return self.properties.get("CanSendLink", None)

    @odata(name="IsUserSiteAdmin")
    @property
    def is_user_site_admin(self) -> Optional[bool]:
        """Boolean that indicates whether or not the current user is a site collection administrator"""
        return self.properties.get("IsUserSiteAdmin", None)

    @odata(name="ListId")
    @property
    def list_id(self) -> Optional[str]:
        """The unique ID of the parent list (if applicable)."""
        return self.properties.get("ListId", None)

    @odata(name="Roles")
    @property
    def roles(self):
        """
        A dictionary object that lists the display name and the id of the SharePoint regular roles.
        """
        return self.properties.get("Roles", None)

    @odata(name="ObjectSharingInformation", navigation=True)
    @property
    def object_sharing_information(self) -> ObjectSharingInformation:
        """
        Contains information about the sharing state of a shareable object.
        """
        return self.properties.get(
            "ObjectSharingInformation",
            ObjectSharingInformation(
                self.context,
                ResourcePath("ObjectSharingInformation", self.resource_path),
            ),
        )

    @odata(name="SharePointSettings", navigation=True)
    @property
    def sharepoint_settings(self) -> SharePointSharingSettings:
        """An object that contains the SharePoint UI specific sharing settings."""
        return self.properties.get(
            "SharePointSettings",
            SharePointSharingSettings(self.context, ResourcePath("SharePointSettings", self.resource_path)),
        )

    @odata(name="SharingPermissions", navigation=True)
    @property
    def sharing_permissions(self) -> SharingPermissionInformation:
        """A list of SharingPermissionInformation objects that can be used to share."""
        return self.properties.get(
            "SharingPermissions",
            SharingPermissionInformation(self.context, ResourcePath("SharingPermissions", self.resource_path)),
        )

    @odata(name="CanCurrentUserManageReadWriteLink")
    @property
    def can_current_user_manage_read_write_link(self) -> Optional[bool]:
        """Gets the CanCurrentUserManageReadWriteLink property"""
        return self.properties.get("CanCurrentUserManageReadWriteLink", None)

    @odata(name="CanCurrentUserRetrieveOrganizationReadonlyLink")
    @property
    def can_current_user_retrieve_organization_readonly_link(self) -> Optional[bool]:
        """Gets the CanCurrentUserRetrieveOrganizationReadonlyLink property"""
        return self.properties.get("CanCurrentUserRetrieveOrganizationReadonlyLink", None)

    @odata(name="CanCurrentUserRetrieveOrganizationReadWriteLink")
    @property
    def can_current_user_retrieve_organization_read_write_link(self) -> Optional[bool]:
        """Gets the CanCurrentUserRetrieveOrganizationReadWriteLink property"""
        return self.properties.get("CanCurrentUserRetrieveOrganizationReadWriteLink", None)

    @odata(name="CanCurrentUserRetrieveReadonlyLink")
    @property
    def can_current_user_retrieve_readonly_link(self) -> Optional[bool]:
        """Gets the CanCurrentUserRetrieveReadonlyLink property"""
        return self.properties.get("CanCurrentUserRetrieveReadonlyLink", None)

    @odata(name="CanCurrentUserRetrieveReadWriteLink")
    @property
    def can_current_user_retrieve_read_write_link(self) -> Optional[bool]:
        """Gets the CanCurrentUserRetrieveReadWriteLink property"""
        return self.properties.get("CanCurrentUserRetrieveReadWriteLink", None)

    @odata(name="CanCurrentUserShareExternally")
    @property
    def can_current_user_share_externally(self) -> Optional[bool]:
        """Gets the CanCurrentUserShareExternally property"""
        return self.properties.get("CanCurrentUserShareExternally", None)

    @odata(name="CanCurrentUserShareInternally")
    @property
    def can_current_user_share_internally(self) -> Optional[bool]:
        """Gets the CanCurrentUserShareInternally property"""
        return self.properties.get("CanCurrentUserShareInternally", None)

    @odata(name="CanCurrentUserShareToExistingGuests")
    @property
    def can_current_user_share_to_existing_guests(self) -> Optional[bool]:
        """Gets the CanCurrentUserShareToExistingGuests property"""
        return self.properties.get("CanCurrentUserShareToExistingGuests", None)

    @odata(name="CanShareFolder")
    @property
    def can_share_folder(self) -> Optional[bool]:
        """Gets the CanShareFolder property"""
        return self.properties.get("CanShareFolder", None)

    @odata(name="DefaultShareLinkPermission")
    @property
    def default_share_link_permission(self) -> Optional[int]:
        """Gets the DefaultShareLinkPermission property"""
        return self.properties.get("DefaultShareLinkPermission", None)

    @odata(name="DefaultShareLinkType")
    @property
    def default_share_link_type(self) -> Optional[int]:
        """Gets the DefaultShareLinkType property"""
        return self.properties.get("DefaultShareLinkType", None)

    @odata(name="EnforceIBSegmentFiltering")
    @property
    def enforce_ib_segment_filtering(self) -> Optional[bool]:
        """Gets the EnforceIBSegmentFiltering property"""
        return self.properties.get("EnforceIBSegmentFiltering", None)

    @odata(name="EnforceSPOSearch")
    @property
    def enforce_spo_search(self) -> Optional[bool]:
        """Gets the EnforceSPOSearch property"""
        return self.properties.get("EnforceSPOSearch", None)

    @odata(name="HasEditRole")
    @property
    def has_edit_role(self) -> Optional[bool]:
        """Gets the HasEditRole property"""
        return self.properties.get("HasEditRole", None)

    @odata(name="HasReadRole")
    @property
    def has_read_role(self) -> Optional[bool]:
        """Gets the HasReadRole property"""
        return self.properties.get("HasReadRole", None)

    @odata(name="InheritingWebLink")
    @property
    def inheriting_web_link(self) -> Optional[str]:
        """Gets the InheritingWebLink property"""
        return self.properties.get("InheritingWebLink", None)

    @odata(name="IsGuestUser")
    @property
    def is_guest_user(self) -> Optional[bool]:
        """Gets the IsGuestUser property"""
        return self.properties.get("IsGuestUser", None)

    @odata(name="IsPictureLibrary")
    @property
    def is_picture_library(self) -> Optional[bool]:
        """Gets the IsPictureLibrary property"""
        return self.properties.get("IsPictureLibrary", None)

    @odata(name="ItemId")
    @property
    def item_id(self) -> Optional[str]:
        """Gets the ItemId property"""
        return self.properties.get("ItemId", None)

    @odata(name="ItemName")
    @property
    def item_name(self) -> Optional[str]:
        """Gets the ItemName property"""
        return self.properties.get("ItemName", None)

    @odata(name="ItemUrl")
    @property
    def item_url(self) -> Optional[str]:
        """Gets the ItemUrl property"""
        return self.properties.get("ItemUrl", None)

    @odata(name="PermissionsOnlyMode")
    @property
    def permissions_only_mode(self) -> Optional[bool]:
        """Gets the PermissionsOnlyMode property"""
        return self.properties.get("PermissionsOnlyMode", None)

    @odata(name="RequiredAnonymousLinkExpirationInDays")
    @property
    def required_anonymous_link_expiration_in_days(self) -> Optional[int]:
        """Gets the RequiredAnonymousLinkExpirationInDays property"""
        return self.properties.get("RequiredAnonymousLinkExpirationInDays", None)

    @odata(name="ShareByEmailEnabled")
    @property
    def share_by_email_enabled(self) -> Optional[bool]:
        """Gets the ShareByEmailEnabled property"""
        return self.properties.get("ShareByEmailEnabled", None)

    @odata(name="ShowExternalSharingWarning")
    @property
    def show_external_sharing_warning(self) -> Optional[bool]:
        """Gets the ShowExternalSharingWarning property"""
        return self.properties.get("ShowExternalSharingWarning", None)

    @odata(name="SiteIBMode")
    @property
    def site_ib_mode(self) -> Optional[str]:
        """Gets the SiteIBMode property"""
        return self.properties.get("SiteIBMode", None)

    @odata(name="SiteIBSegmentIDs")
    @property
    def site_ib_segment_ids(self) -> StringCollection:
        """Gets the SiteIBSegmentIDs property"""
        return self.properties.get("SiteIBSegmentIDs", StringCollection())

    @odata(name="SupportsAclPropagation")
    @property
    def supports_acl_propagation(self) -> Optional[bool]:
        """Gets the SupportsAclPropagation property"""
        return self.properties.get("SupportsAclPropagation", None)
