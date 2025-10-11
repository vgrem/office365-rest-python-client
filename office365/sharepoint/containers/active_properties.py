from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.containers.spactivecontainermemberproperties import (
    SPActiveContainerMemberProperties,
)


class SPActiveContainerProperties(ClientValue):

    def __init__(
        self,
        application_name: str = None,
        archived_by: str = None,
        archive_status: str = None,
        container_api_url: str = None,
        container_id: str = None,
        container_name: str = None,
        container_site_url: str = None,
        container_type_id: str = None,
        created_by: str = None,
        created_on: str = None,
        deleted_on: str = None,
        description: str = None,
        last_archived_date_time: str = None,
        optical_character_recognition_enabled: bool = None,
        owners: ClientValueCollection[SPActiveContainerMemberProperties] = ClientValueCollection(
            SPActiveContainerMemberProperties
        ),
        owners_count: int = None,
        ownership_type: str = None,
        owning_application_id: str = None,
        principal_owner_identifier: str = None,
        publisher_name: str = None,
        readers: ClientValueCollection[SPActiveContainerMemberProperties] = ClientValueCollection(
            SPActiveContainerMemberProperties
        ),
        sensitivity_label: str = None,
        status: str = None,
        storage_used: int = None,
        writers: ClientValueCollection[SPActiveContainerMemberProperties] = ClientValueCollection(
            SPActiveContainerMemberProperties
        ),
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
