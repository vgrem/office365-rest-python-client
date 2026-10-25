from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class AppInstanceErrorDetails(Entity):
    @odata(name="CorrelationId")
    @property
    def correlation_id(self) -> Optional[UUID]:
        """Gets the CorrelationId property"""
        return self.properties.get("CorrelationId", None)

    @odata(name="ErrorDetail")
    @property
    def error_detail(self) -> Optional[str]:
        """Gets the ErrorDetail property"""
        return self.properties.get("ErrorDetail", None)

    @odata(name="ErrorType")
    @property
    def error_type(self) -> Optional[int]:
        """Gets the ErrorType property"""
        return self.properties.get("ErrorType", None)

    @odata(name="ErrorTypeName")
    @property
    def error_type_name(self) -> Optional[str]:
        """Gets the ErrorTypeName property"""
        return self.properties.get("ErrorTypeName", None)

    @odata(name="ExceptionMessage")
    @property
    def exception_message(self) -> Optional[str]:
        """Gets the ExceptionMessage property"""
        return self.properties.get("ExceptionMessage", None)

    @odata(name="Source")
    @property
    def source(self) -> Optional[int]:
        """Gets the Source property"""
        return self.properties.get("Source", None)

    @odata(name="SourceName")
    @property
    def source_name(self) -> Optional[str]:
        """Gets the SourceName property"""
        return self.properties.get("SourceName", None)
