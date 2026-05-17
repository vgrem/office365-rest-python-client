from enum import Enum


class OnenoteSourceService(Enum):
    Unknown = "0"
    OneDrive = "1"
    OneDriveForBusiness = "2"
    OnPremOneDriveForBusiness = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnenoteSourceService"
