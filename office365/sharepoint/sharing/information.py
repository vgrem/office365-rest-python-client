from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.sharing.abilities import SharingAbilities
from office365.sharepoint.sharing.access_request_settings import AccessRequestSettings
from office365.sharepoint.sharing.address_bar_link_settings import AddressBarLinkSettings
from office365.sharepoint.sharing.domain_restriction_settings import (
    DomainRestrictionSettings,
)
from office365.sharepoint.sharing.itemsharingsettings import ItemSharingSettings
from office365.sharepoint.sharing.links.default_templates_collection import (
    SharingLinkDefaultTemplatesCollection,
)
from office365.sharepoint.sharing.permission_collection import PermissionCollection
from office365.sharepoint.sharing.picker_settings import PickerSettings
from office365.sharepoint.sharing.recipient_limits import RecipientLimits
from office365.sharepoint.sharing.sensitivitylabelinformation import SensitivityLabelInformation
from office365.sharepoint.sharing.uniqueaccessgroupswrapper import UniqueAccessGroupsWrapper


class SharingInformation(Entity):
    """Represents a response for Microsoft.SharePoint.Client.Sharing.SecurableObjectExtensions.GetSharingInformation.
    The accessRequestSettings, domainRestrictionSettings and permissionsInformation properties are not included in
    the default scalar property set for this type.
    """

    @odata(name="accessRequestSettings")
    @property
    def access_request_settings(self) -> AccessRequestSettings:
        """
        AccessRequestSettings is an optional property set to retrieve details for pending access requests if present.
        """
        return self.properties.get("accessRequestSettings", AccessRequestSettings())

    @odata(name="anonymousLinkExpirationRestrictionDays")
    @property
    def anonymous_link_expiration_restriction_days(self) -> Optional[int]:
        """Tenant's anonymous link expiration restriction in days."""
        return self.properties.get("anonymousLinkExpirationRestrictionDays", None)

    @odata(name="domainRestrictionSettings")
    @property
    def domain_restriction_settings(self) -> DomainRestrictionSettings:
        """Whether DomainRestrictionSettings is used to limit the external Users set by Admin."""
        return self.properties.get("domainRestrictionSettings", DomainRestrictionSettings())

    @odata(name="permissionsInformation")
    @property
    def permissions_information(self) -> PermissionCollection:
        """
        The PermissionCollection that are on the list item. It contains a collection of PrincipalInfo and LinkInfo.
        """
        return self.properties.get("permissionsInformation", PermissionCollection())

    @odata(name="pickerSettings", navigation=True)
    @property
    def picker_settings(self):
        """PickerSettings used by the PeoplePicker Control."""
        return self.properties.get(
            "pickerSettings",
            PickerSettings(self.context, ResourcePath("pickerSettings", self.resource_path)),
        )

    @odata(name="sharingAbilities", beta=True)
    @property
    def sharing_abilities(self) -> SharingAbilities:
        """
        Matrix of possible sharing abilities per sharing type and the state of each capability for the current user
        on the list item."""
        return self.properties.get("sharingAbilities", SharingAbilities())

    @odata(name="sharingLinkTemplates")
    @property
    def sharing_link_templates(self) -> SharingLinkDefaultTemplatesCollection:
        """"""
        return self.properties.get("sharingLinkTemplates", SharingLinkDefaultTemplatesCollection())

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "accessRequestSettings": self.access_request_settings,
                "domain_restriction_settings": self.domain_restriction_settings,
                "permissionsInformation": self.permissions_information,
                "pickerSettings": self.picker_settings,
                "sharingAbilities": self.sharing_abilities,
                "sharingLinkTemplates": self.sharing_link_templates,
            }
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingInformation"

    @odata(name="addressBarLinkSettings", beta=True)
    @property
    def address_bar_link_settings(self) -> AddressBarLinkSettings:
        """Gets the addressBarLinkSettings property"""
        return self.properties.get("addressBarLinkSettings", AddressBarLinkSettings())

    @odata(name="ageGroup", beta=True)
    @property
    def age_group(self) -> Optional[int]:
        """Gets the ageGroup property"""
        return self.properties.get("ageGroup", None)

    @odata(name="allOrganizationSecurityGroupId", beta=True)
    @property
    def all_organization_security_group_id(self) -> Optional[UUID]:
        """Gets the allOrganizationSecurityGroupId property"""
        return self.properties.get("allOrganizationSecurityGroupId", None)

    @odata(name="anyoneLinkTrackUsers")
    @property
    def anyone_link_track_users(self) -> Optional[bool]:
        """Gets the anyoneLinkTrackUsers property"""
        return self.properties.get("anyoneLinkTrackUsers", None)

    @odata(name="blockPeoplePickerAndSharing")
    @property
    def block_people_picker_and_sharing(self) -> Optional[bool]:
        """Gets the blockPeoplePickerAndSharing property"""
        return self.properties.get("blockPeoplePickerAndSharing", None)

    @odata(name="canAddExistingExternalPrincipal")
    @property
    def can_add_existing_external_principal(self) -> Optional[bool]:
        """Gets the canAddExistingExternalPrincipal property"""
        return self.properties.get("canAddExistingExternalPrincipal", None)

    @odata(name="canAddExternalPrincipal")
    @property
    def can_add_external_principal(self) -> Optional[bool]:
        """Gets the canAddExternalPrincipal property"""
        return self.properties.get("canAddExternalPrincipal", None)

    @odata(name="canAddInternalPrincipal")
    @property
    def can_add_internal_principal(self) -> Optional[bool]:
        """Gets the canAddInternalPrincipal property"""
        return self.properties.get("canAddInternalPrincipal", None)

    @odata(name="canRequestAccessForGrantAccess")
    @property
    def can_request_access_for_grant_access(self) -> Optional[bool]:
        """Gets the canRequestAccessForGrantAccess property"""
        return self.properties.get("canRequestAccessForGrantAccess", None)

    @odata(name="canSendEmail")
    @property
    def can_send_email(self) -> Optional[bool]:
        """Gets the canSendEmail property"""
        return self.properties.get("canSendEmail", None)

    @odata(name="canUseSimplifiedRoles")
    @property
    def can_use_simplified_roles(self) -> Optional[bool]:
        """Gets the canUseSimplifiedRoles property"""
        return self.properties.get("canUseSimplifiedRoles", None)

    @odata(name="currentRole")
    @property
    def current_role(self) -> Optional[int]:
        """Gets the currentRole property"""
        return self.properties.get("currentRole", None)

    @odata(name="customizedExternalSharingServiceUrl")
    @property
    def customized_external_sharing_service_url(self) -> Optional[str]:
        """Gets the customizedExternalSharingServiceUrl property"""
        return self.properties.get("customizedExternalSharingServiceUrl", None)

    @odata(name="defaultLinkKind")
    @property
    def default_link_kind(self) -> Optional[int]:
        """Gets the defaultLinkKind property"""
        return self.properties.get("defaultLinkKind", None)

    @odata(name="defaultShareLinkPermission")
    @property
    def default_share_link_permission(self) -> Optional[int]:
        """Gets the defaultShareLinkPermission property"""
        return self.properties.get("defaultShareLinkPermission", None)

    @odata(name="defaultShareLinkScope")
    @property
    def default_share_link_scope(self) -> Optional[int]:
        """Gets the defaultShareLinkScope property"""
        return self.properties.get("defaultShareLinkScope", None)

    @odata(name="defaultShareLinkToExistingAccess")
    @property
    def default_share_link_to_existing_access(self) -> Optional[bool]:
        """Gets the defaultShareLinkToExistingAccess property"""
        return self.properties.get("defaultShareLinkToExistingAccess", None)

    @odata(name="directUrl")
    @property
    def direct_url(self) -> Optional[str]:
        """Gets the directUrl property"""
        return self.properties.get("directUrl", None)

    @odata(name="directUrlLegacy")
    @property
    def direct_url_legacy(self) -> Optional[str]:
        """Gets the directUrlLegacy property"""
        return self.properties.get("directUrlLegacy", None)

    @odata(name="discoverableByOrganizationEnabled", beta=True)
    @property
    def discoverable_by_organization_enabled(self) -> Optional[bool]:
        """Gets the discoverableByOrganizationEnabled property"""
        return self.properties.get("discoverableByOrganizationEnabled", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="enforceIBSegmentFiltering", beta=True)
    @property
    def enforce_ib_segment_filtering(self) -> Optional[bool]:
        """Gets the enforceIBSegmentFiltering property"""
        return self.properties.get("enforceIBSegmentFiltering", None)

    @odata(name="enforceSPOSearch", beta=True)
    @property
    def enforce_spo_search(self) -> Optional[bool]:
        """Gets the enforceSPOSearch property"""
        return self.properties.get("enforceSPOSearch", None)

    @odata(name="fileExtension", beta=True)
    @property
    def file_extension(self) -> Optional[str]:
        """Gets the fileExtension property"""
        return self.properties.get("fileExtension", None)

    @odata(name="hasUniquePermissions")
    @property
    def has_unique_permissions(self) -> Optional[bool]:
        """Gets the hasUniquePermissions property"""
        return self.properties.get("hasUniquePermissions", None)

    @odata(name="isConsumerFiles", beta=True)
    @property
    def is_consumer_files(self) -> Optional[bool]:
        """Gets the isConsumerFiles property"""
        return self.properties.get("isConsumerFiles", None)

    @odata(name="isMultiTenantOrganization")
    @property
    def is_multi_tenant_organization(self) -> Optional[bool]:
        """Gets the isMultiTenantOrganization property"""
        return self.properties.get("isMultiTenantOrganization", None)

    @odata(name="isPremium", beta=True)
    @property
    def is_premium(self) -> Optional[bool]:
        """Gets the isPremium property"""
        return self.properties.get("isPremium", None)

    @odata(name="isStubFile", beta=True)
    @property
    def is_stub_file(self) -> Optional[bool]:
        """Gets the isStubFile property"""
        return self.properties.get("isStubFile", None)

    @odata(name="itemUniqueId")
    @property
    def item_unique_id(self) -> Optional[UUID]:
        """Gets the itemUniqueId property"""
        return self.properties.get("itemUniqueId", None)

    @odata(name="itemUrl")
    @property
    def item_url(self) -> Optional[str]:
        """Gets the itemUrl property"""
        return self.properties.get("itemUrl", None)

    @odata(name="listId")
    @property
    def list_id(self) -> Optional[UUID]:
        """Gets the listId property"""
        return self.properties.get("listId", None)

    @odata(name="microserviceShareUiUrl")
    @property
    def microservice_share_ui_url(self) -> Optional[str]:
        """Gets the microserviceShareUiUrl property"""
        return self.properties.get("microserviceShareUiUrl", None)

    @odata(name="outlookEndpointHostUrl")
    @property
    def outlook_endpoint_host_url(self) -> Optional[str]:
        """Gets the outlookEndpointHostUrl property"""
        return self.properties.get("outlookEndpointHostUrl", None)

    @odata(name="recipientLimits", beta=True)
    @property
    def recipient_limits(self) -> RecipientLimits:
        """Gets the recipientLimits property"""
        return self.properties.get("recipientLimits", RecipientLimits())

    @odata(name="sensitivityLabelInformation", beta=True)
    @property
    def sensitivity_label_information(self) -> SensitivityLabelInformation:
        """Gets the sensitivityLabelInformation property"""
        return self.properties.get("sensitivityLabelInformation", SensitivityLabelInformation())

    @odata(name="sharedObjectType")
    @property
    def shared_object_type(self) -> Optional[int]:
        """Gets the sharedObjectType property"""
        return self.properties.get("sharedObjectType", None)

    @odata(name="shareUiUrl")
    @property
    def share_ui_url(self) -> Optional[str]:
        """Gets the shareUiUrl property"""
        return self.properties.get("shareUiUrl", None)

    @odata(name="sharingSettings")
    @property
    def sharing_settings(self) -> ItemSharingSettings:
        """Gets the sharingSettings property"""
        return self.properties.get("sharingSettings", ItemSharingSettings())

    @odata(name="sharingStatus")
    @property
    def sharing_status(self) -> Optional[int]:
        """Gets the sharingStatus property"""
        return self.properties.get("sharingStatus", None)

    @odata(name="showExternalSharingWarning")
    @property
    def show_external_sharing_warning(self) -> Optional[bool]:
        """Gets the showExternalSharingWarning property"""
        return self.properties.get("showExternalSharingWarning", None)

    @odata(name="siteIBMode", beta=True)
    @property
    def site_ib_mode(self) -> Optional[str]:
        """Gets the siteIBMode property"""
        return self.properties.get("siteIBMode", None)

    @odata(name="siteIBSegmentIDs", beta=True)
    @property
    def site_ib_segment_ids(self) -> StringCollection:
        """Gets the siteIBSegmentIDs property"""
        return self.properties.get("siteIBSegmentIDs", StringCollection())

    @odata(name="siteId")
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the siteId property"""
        return self.properties.get("siteId", None)

    @odata(name="standardRolesModified")
    @property
    def standard_roles_modified(self) -> Optional[bool]:
        """Gets the standardRolesModified property"""
        return self.properties.get("standardRolesModified", None)

    @odata(name="substrateFileId")
    @property
    def substrate_file_id(self) -> Optional[str]:
        """Gets the substrateFileId property"""
        return self.properties.get("substrateFileId", None)

    @odata(name="tenantDisplayName")
    @property
    def tenant_display_name(self) -> Optional[str]:
        """Gets the tenantDisplayName property"""
        return self.properties.get("tenantDisplayName", None)

    @odata(name="tenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @odata(name="uniqueAccessGroups", beta=True)
    @property
    def unique_access_groups(self) -> UniqueAccessGroupsWrapper:
        """Gets the uniqueAccessGroups property"""
        return self.properties.get("uniqueAccessGroups", UniqueAccessGroupsWrapper())

    @odata(name="userIsSharingViaMCS")
    @property
    def user_is_sharing_via_mcs(self) -> Optional[str]:
        """Gets the userIsSharingViaMCS property"""
        return self.properties.get("userIsSharingViaMCS", None)

    @odata(name="userPhotoCdnBaseUrl", beta=True)
    @property
    def user_photo_cdn_base_url(self) -> Optional[str]:
        """Gets the userPhotoCdnBaseUrl property"""
        return self.properties.get("userPhotoCdnBaseUrl", None)

    @odata(name="webTemplateId")
    @property
    def web_template_id(self) -> Optional[int]:
        """Gets the webTemplateId property"""
        return self.properties.get("webTemplateId", None)

    @odata(name="webUrl")
    @property
    def web_url(self) -> Optional[str]:
        """Gets the webUrl property"""
        return self.properties.get("webUrl", None)
