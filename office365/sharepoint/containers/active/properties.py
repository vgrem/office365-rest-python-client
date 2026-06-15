from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.containers.active.memberproperties import SPActiveContainerMemberProperties


@dataclass
class SPActiveContainerProperties(ClientValue):
    ApplicationName: Optional[str] = None
    ArchivedBy: Optional[str] = None
    ArchiveStatus: Optional[str] = None
    ContainerApiUrl: Optional[str] = None
    ContainerId: Optional[str] = None
    ContainerName: Optional[str] = None
    ContainerSiteUrl: Optional[str] = None
    ContainerTypeId: Optional[str] = None
    CreatedBy: Optional[str] = None
    CreatedOn: Optional[str] = None
    DeletedOn: Optional[str] = None
    Description: Optional[str] = None
    LastArchivedDateTime: Optional[str] = None
    OpticalCharacterRecognitionEnabled: Optional[bool] = None
    Owners: ClientValueCollection[SPActiveContainerMemberProperties] = field(
        default_factory=lambda: ClientValueCollection(SPActiveContainerMemberProperties)
    )
    OwnersCount: Optional[int] = None
    OwnershipType: Optional[str] = None
    OwningApplicationId: Optional[str] = None
    PrincipalOwnerIdentifier: Optional[str] = None
    PublisherName: Optional[str] = None
    Readers: ClientValueCollection[SPActiveContainerMemberProperties] = field(
        default_factory=lambda: ClientValueCollection(SPActiveContainerMemberProperties)
    )
    SensitivityLabel: Optional[str] = None
    Status: Optional[str] = None
    StorageUsed: Optional[int] = None
    Writers: ClientValueCollection[SPActiveContainerMemberProperties] = field(
        default_factory=lambda: ClientValueCollection(SPActiveContainerMemberProperties)
    )
    ContainerRedirectUrl: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Containers.SPActiveContainerProperties"
