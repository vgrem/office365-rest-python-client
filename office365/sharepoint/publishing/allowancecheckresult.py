from typing import Optional

from office365.sharepoint.entity import Entity


class AllowanceCheckResult(Entity):

    @property
    def allowed(self) -> Optional[bool]:
        """Gets the Allowed property"""
        return self.properties.get("Allowed", None)

    @property
    def error_reason(self) -> Optional[str]:
        """Gets the ErrorReason property"""
        return self.properties.get("ErrorReason", None)

    @property
    def error_code(self) -> Optional[str]:
        """Gets the ErrorCode property"""
        return self.properties.get("ErrorCode", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.AllowanceCheckResult"
