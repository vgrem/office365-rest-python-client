from typing import Optional

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class InformationRightsManagementFileSettings(Entity):
    """Represents the Information Rights Management (IRM) settings of a file."""

    def reset(self) -> Self:
        """Resets all properties to the default value."""
        qry = ServiceOperationQuery(self, "Reset")
        self.context.add_query(qry)
        return self

    @property
    def allow_print(self) -> Optional[bool]:
        """
        Gets a value indicating whether or not the user can print the downloaded document.
        True if print is allowed; otherwise, it is false. The default value is false.
        """
        return self.properties.get("AllowPrint", None)

    @allow_print.setter
    def allow_print(self, value: bool) -> None:
        """
        Sets a value indicating whether or not the user can print the downloaded document.
        """
        self.set_property("AllowPrint", value)

    @property
    def allow_script(self) -> Optional[bool]:
        """
        Gets a value indicating whether or not the user can run a script on the downloaded document.
        True if the script is allowed to run; otherwise, it is false. The default value is false.
        """
        return self.properties.get("AllowScript", None)

    @allow_script.setter
    def allow_script(self, value: bool) -> None:
        """
        Sets a value indicating whether or not the user can run a script on the downloaded document.
        """
        self.set_property("AllowPrint", value)

    @property
    def allow_write_copy(self) -> Optional[bool]:
        """
        Gets value indicating whether or not the user can write on a copy of the downloaded document.
        True if write on a copy is allowed; otherwise, it is false. The default value is false.
        """
        return self.properties.get("AllowWriteCopy", None)

    @property
    def disable_document_browser_view(self) -> Optional[bool]:
        """
        Specifies whether to block the Office Add-in from showing this document. The default value is false.
        """
        return self.properties.get("DisableDocumentBrowserView", None)

    @property
    def document_access_expire_days(self) -> Optional[int]:
        """
        Specifies the number of days after which the downloaded document will expire.
        """
        return self.properties.get("DocumentAccessExpireDays", None)

    @property
    def enable_document_access_expire(self) -> Optional[bool]:
        """
        Specifies whether the downloaded document will expire.
        """
        return self.properties.get("EnableDocumentAccessExpire", None)
