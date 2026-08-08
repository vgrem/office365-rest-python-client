from enum import Enum


class AuditLogUserType(Enum):
    Regular = "0"
    Reserved = "1"
    Admin = "2"
    DcAdmin = "3"
    System = "4"
    Application = "5"
    ServicePrincipal = "6"
    CustomPolicy = "7"
    SystemPolicy = "8"
    PartnerTechnician = "9"
    Guest = "10"
    unknownFutureValue = "11"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AuditLogUserType"
