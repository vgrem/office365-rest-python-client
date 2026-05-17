from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from typing import Optional


class SPContainerFilterOrder(ClientValue):
    def __init__(
        self,
        archive_status: Optional[int] = None,
        created_before_days: Optional[int] = None,
        deleted_before_days: Optional[int] = None,
        filtering_application_id: Optional[str] = None,
        filtering_application_name: Optional[str] = None,
        filtering_container_type_id: Optional[str] = None,
        filtering_field: Optional[int] = None,
        filtering_sensitivity_labels: StringCollection = StringCollection(),
        optical_character_recognition_enabled: Optional[bool] = None,
        owners_count: Optional[int] = None,
        ownership_type: Optional[int] = None,
        principal_owner_identifier: Optional[str] = None,
        publisher_name: Optional[str] = None,
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
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerFilterOrder"
