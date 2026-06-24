from office365.runtime.client_value import ClientValue


class OperationError(ClientValue):
    code: str | None = None
    message: str | None = None
    "Represents the error information for a failed Teams async operation."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OperationError"
