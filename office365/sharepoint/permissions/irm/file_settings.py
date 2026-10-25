from __future__ import annotations

from typing import Optional

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class InformationRightsManagementFileSettings(Entity):
    """Represents the Information Rights Management (IRM) settings of a file."""

    def reset(self) -> Self:
        """Resets all properties to the default value."""
        qry = ServiceOperationQuery(self, "Reset")
        self.context.add_query(qry)
        return self

    @odata(name="AllowPrint")
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

    @odata(name="AllowScript")
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

    @odata(name="AllowWriteCopy")
    @property
    def allow_write_copy(self) -> Optional[bool]:
        """
        Gets value indicating whether or not the user can write on a copy of the downloaded document.
        True if write on a copy is allowed; otherwise, it is false. The default value is false.
        """
        return self.properties.get("AllowWriteCopy", None)

    @odata(name="DisableDocumentBrowserView")
    @property
    def disable_document_browser_view(self) -> Optional[bool]:
        """
        Specifies whether to block the Office Add-in from showing this document. The default value is false.
        """
        return self.properties.get("DisableDocumentBrowserView", None)

    @odata(name="DocumentAccessExpireDays")
    @property
    def document_access_expire_days(self) -> Optional[int]:
        """
        Specifies the number of days after which the downloaded document will expire.
        """
        return self.properties.get("DocumentAccessExpireDays", None)

    @odata(name="EnableDocumentAccessExpire")
    @property
    def enable_document_access_expire(self) -> Optional[bool]:
        """
        Specifies whether the downloaded document will expire.
        """
        return self.properties.get("EnableDocumentAccessExpire", None)

    @odata(name="EnableDocumentBrowserPublishingView")
    @property
    def enable_document_browser_publishing_view(self) -> Optional[bool]:
        """Gets the EnableDocumentBrowserPublishingView property"""
        return self.properties.get("EnableDocumentBrowserPublishingView", None)

    @odata(name="EnableGroupProtection")
    @property
    def enable_group_protection(self) -> Optional[bool]:
        """Gets the EnableGroupProtection property"""
        return self.properties.get("EnableGroupProtection", None)

    @odata(name="EnableLicenseCacheExpire")
    @property
    def enable_license_cache_expire(self) -> Optional[bool]:
        """Gets the EnableLicenseCacheExpire property"""
        return self.properties.get("EnableLicenseCacheExpire", None)

    @odata(name="GroupName")
    @property
    def group_name(self) -> Optional[str]:
        """Gets the GroupName property"""
        return self.properties.get("GroupName", None)

    @odata(name="IrmEnabled")
    @property
    def irm_enabled(self) -> Optional[bool]:
        """Gets the IrmEnabled property"""
        return self.properties.get("IrmEnabled", None)

    @odata(name="LicenseCacheExpireDays")
    @property
    def license_cache_expire_days(self) -> Optional[int]:
        """Gets the LicenseCacheExpireDays property"""
        return self.properties.get("LicenseCacheExpireDays", None)

    @odata(name="PolicyDescription")
    @property
    def policy_description(self) -> Optional[str]:
        """Gets the PolicyDescription property"""
        return self.properties.get("PolicyDescription", None)

    @odata(name="PolicyTitle")
    @property
    def policy_title(self) -> Optional[str]:
        """Gets the PolicyTitle property"""
        return self.properties.get("PolicyTitle", None)

    @odata(name="TemplateId")
    @property
    def template_id(self) -> Optional[str]:
        """Gets the TemplateId property"""
        return self.properties.get("TemplateId", None)
