from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.containers.active.memberproperties import (
    SPActiveContainerMemberProperties,
)


class SPActiveContainerProperties(ClientValue):
    def __init__(
        self,
        application_name: Optional[str] = None,
        archived_by: Optional[str] = None,
        archive_status: Optional[str] = None,
        container_api_url: Optional[str] = None,
        container_id: Optional[str] = None,
        container_name: Optional[str] = None,
        container_site_url: Optional[str] = None,
        container_type_id: Optional[str] = None,
        created_by: Optional[str] = None,
        created_on: Optional[str] = None,
        deleted_on: Optional[str] = None,
        description: Optional[str] = None,
        last_archived_date_time: Optional[str] = None,
        optical_character_recognition_enabled: Optional[bool] = None,
        owners: ClientValueCollection[SPActiveContainerMemberProperties] = ClientValueCollection(
            SPActiveContainerMemberProperties
        ),
        owners_count: Optional[int] = None,
        ownership_type: Optional[str] = None,
        owning_application_id: Optional[str] = None,
        principal_owner_identifier: Optional[str] = None,
        publisher_name: Optional[str] = None,
        readers: ClientValueCollection[SPActiveContainerMemberProperties] = ClientValueCollection(
            SPActiveContainerMemberProperties
        ),
        sensitivity_label: Optional[str] = None,
        status: Optional[str] = None,
        storage_used: Optional[int] = None,
    ):
        self.ApplicationName = application_name
        self.ArchivedBy = archived_by
        self.ArchiveStatus = archive_status
        self.ContainerApiUrl = container_api_url
        self.ContainerId = container_id
        self.ContainerName = container_name
        self.ContainerSiteUrl = container_site_url
        self.ContainerTypeId = container_type_id
        self.CreatedBy = created_by
        self.CreatedOn = created_on
        self.DeletedOn = deleted_on
        self.Description = description
        self.LastArchivedDateTime = last_archived_date_time
        self.OpticalCharacterRecognitionEnabled = optical_character_recognition_enabled
        self.Owners = owners
        self.OwnersCount = owners_count
        self.OwnershipType = ownership_type
        self.OwningApplicationId = owning_application_id
        self.PrincipalOwnerIdentifier = principal_owner_identifier
        self.PublisherName = publisher_name
        self.Readers = readers
        self.SensitivityLabel = sensitivity_label
        self.Status = status
        self.StorageUsed = storage_used
        self.Writers = writers

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Containers.SPActiveContainerProperties"
