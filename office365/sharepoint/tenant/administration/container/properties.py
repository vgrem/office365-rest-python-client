from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from typing import Optional


class SPContainerProperties(ClientValue):
    """"""

    def __init__(
        self,
        allow_editing: Optional[bool] = None,
        archived_by: Optional[str] = None,
        archive_status: Optional[int] = None,
        authentication_context_name: Optional[str] = None,
        block_download_policy: Optional[bool] = None,
        conditional_access_policy: Optional[int] = None,
        container_api_url: Optional[str] = None,
        container_id: Optional[str] = None,
        container_name: Optional[str] = None,
        container_site_url: Optional[str] = None,
        container_type_id: Optional[UUID] = None,
        created_by: Optional[str] = None,
        created_on: Optional[datetime] = None,
        description: Optional[str] = None,
        exclude_block_download_policy_container_owners: Optional[bool] = None,
        last_archived_date_time: Optional[datetime] = None,
        limited_access_file_type: Optional[int] = None,
        managers: Optional[StringCollection] = None,
        new_principal_owner_identifier: Optional[str] = None,
        owners: Optional[StringCollection] = None,
        owners_count: Optional[int] = None,
        ownership_type: Optional[str] = None,
        owning_application_id: Optional[UUID] = None,
        owning_application_name: Optional[str] = None,
        principal_owner_identifier: Optional[str] = None,
        readers: Optional[StringCollection] = None,
        read_only_for_block_download_policy: Optional[bool] = None,
        read_only_for_unmanaged_devices: Optional[bool] = None,
        sensitivity_label: Optional[str] = None,
        sharing_allowed_domain_list: Optional[str] = None,
        sharing_blocked_domain_list: Optional[str] = None,
        sharing_domain_restriction_mode: Optional[int] = None,
        status: Optional[str] = None,
        storage_used: Optional[int] = None,
        transfer_from_principal_owner_identifier: Optional[str] = None,
        writers: StringCollection = StringCollection(),
        restrict_content_org_wide_search: Optional[bool] = None,
    ):
        self.AllowEditing = allow_editing
        self.ArchivedBy = archived_by
        self.ArchiveStatus = archive_status
        self.AuthenticationContextName = authentication_context_name
        self.BlockDownloadPolicy = block_download_policy
        self.ConditionalAccessPolicy = conditional_access_policy
        self.ContainerApiUrl = container_api_url
        self.ContainerId = container_id
        self.ContainerName = container_name
        self.ContainerSiteUrl = container_site_url
        self.ContainerTypeId = container_type_id
        self.CreatedBy = created_by
        self.CreatedOn = created_on
        self.Description = description
        self.ExcludeBlockDownloadPolicyContainerOwners = exclude_block_download_policy_container_owners
        self.LastArchivedDateTime = last_archived_date_time
        self.LimitedAccessFileType = limited_access_file_type
        self.Managers = managers
        self.NewPrincipalOwnerIdentifier = new_principal_owner_identifier
        self.Owners = owners
        self.OwnersCount = owners_count
        self.OwnershipType = ownership_type
        self.OwningApplicationId = owning_application_id
        self.OwningApplicationName = owning_application_name
        self.PrincipalOwnerIdentifier = principal_owner_identifier
        self.Readers = readers
        self.ReadOnlyForBlockDownloadPolicy = read_only_for_block_download_policy
        self.ReadOnlyForUnmanagedDevices = read_only_for_unmanaged_devices
        self.SensitivityLabel = sensitivity_label
        self.SharingAllowedDomainList = sharing_allowed_domain_list
        self.SharingBlockedDomainList = sharing_blocked_domain_list
        self.SharingDomainRestrictionMode = sharing_domain_restriction_mode
        self.Status = status
        self.StorageUsed = storage_used
        self.TransferFromPrincipalOwnerIdentifier = transfer_from_principal_owner_identifier
        self.Writers = writers
        self.RestrictContentOrgWideSearch = restrict_content_org_wide_search

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerProperties"
