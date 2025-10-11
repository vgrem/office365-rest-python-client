from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class SPContainerFilterOrder(ClientValue):

    def __init__(
        self,
        archive_status: int = None,
        created_before_days: int = None,
        deleted_before_days: int = None,
        filtering_application_id: str = None,
        filtering_application_name: str = None,
        filtering_container_type_id: str = None,
        filtering_field: int = None,
        filtering_sensitivity_labels: StringCollection = StringCollection(),
        optical_character_recognition_enabled: bool = None,
        owners_count: int = None,
        ownership_type: int = None,
        principal_owner_identifier: str = None,
        publisher_name: str = None,
    ):
        self.ArchiveStatus = archive_status
        self.CreatedBeforeDays = created_before_days
        self.DeletedBeforeDays = deleted_before_days
        self.FilteringApplicationId = filtering_application_id
        self.FilteringApplicationName = filtering_application_name
        self.FilteringContainerTypeId = filtering_container_type_id
        self.FilteringField = filtering_field
        self.FilteringSensitivityLabels = filtering_sensitivity_labels
        self.OpticalCharacterRecognitionEnabled = optical_character_recognition_enabled
        self.OwnersCount = owners_count
        self.OwnershipType = ownership_type
        self.PrincipalOwnerIdentifier = principal_owner_identifier
        self.PublisherName = publisher_name

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerFilterOrder"
