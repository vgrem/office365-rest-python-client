from office365.runtime.client_value import ClientValue


class ServiceStatus(ClientValue):
    stopped = "1"
    starting = "2"
    running = "3"
    disabled = "4"
    onboarding = "5"
    unknown = "6"
    unknownFutureValue = "7"
    "Represents the tenant-level service status of the backup service."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.ServiceStatus"
