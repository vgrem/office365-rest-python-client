from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class AppInstanceErrorDetails(Entity):
    @property
    def correlation_id(self) -> Optional[UUID]:
        """Gets the CorrelationId property"""
        return self.properties.get("CorrelationId", None)

    @property
    def error_detail(self) -> Optional[str]:
        """Gets the ErrorDetail property"""
        return self.properties.get("ErrorDetail", None)

    @property
    def error_type(self) -> Optional[int]:
        """Gets the ErrorType property"""
        return self.properties.get("ErrorType", None)

    @property
    def error_type_name(self) -> Optional[str]:
        """Gets the ErrorTypeName property"""
        return self.properties.get("ErrorTypeName", None)

    @property
    def exception_message(self) -> Optional[str]:
        """Gets the ExceptionMessage property"""
        return self.properties.get("ExceptionMessage", None)

    @property
    def source(self) -> Optional[int]:
        """Gets the Source property"""
        return self.properties.get("Source", None)

    @property
    def source_name(self) -> Optional[str]:
        """Gets the SourceName property"""
        return self.properties.get("SourceName", None)
