from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SPContainerProperties(ClientValue):
    """"""

    def __init__(
        self,
        allow_editing: bool = None,
        archived_by: str = None,
        archive_status: int = None,
        authentication_context_name: str = None,
        block_download_policy: bool = None,
        conditional_access_policy: int = None,
        container_api_url: str = None,
        container_id: str = None,
        container_name: str = None,
        container_site_url: str = None,
        container_type_id: UUID = None,
        created_by: str = None,
        created_on: datetime = None,
        description: str = None,
        exclude_block_download_policy_container_owners: bool = None,
        last_archived_date_time: datetime = None,
        limited_access_file_type: int = None,
        managers: StringCollection = None,
        new_principal_owner_identifier: str = None,
        owners: StringCollection = None,
        owners_count: int = None,
        ownership_type: str = None,
        owning_application_id: UUID = None,
        owning_application_name: str = None,
        principal_owner_identifier: str = None,
        readers: StringCollection = None,
        read_only_for_block_download_policy: bool = None,
        read_only_for_unmanaged_devices: bool = None,
        sensitivity_label: str = None,
        sharing_allowed_domain_list: str = None,
        sharing_blocked_domain_list: str = None,
        sharing_domain_restriction_mode: int = None,
        status: str = None,
        storage_used: int = None,
        transfer_from_principal_owner_identifier: str = None,
        writers: StringCollection = StringCollection(),
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
        self.ExcludeBlockDownloadPolicyContainerOwners = (
            exclude_block_download_policy_container_owners
        )
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
        self.TransferFromPrincipalOwnerIdentifier = (
            transfer_from_principal_owner_identifier
        )
        self.Writers = writers

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerProperties"
