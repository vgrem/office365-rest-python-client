from __future__ import annotations

import datetime
from typing import Optional

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class InformationRightsManagementSettings(Entity):
    """Represents the Information Rights Management (IRM) settings of a list in Microsoft SharePoint Foundation."""

    @odata(name="AllowPrint")
    @property
    def allow_print(self) -> Optional[bool]:
        """Specifies whether a user can print the downloaded document."""
        return self.properties.get("AllowPrint", None)

    @odata(name="AllowScript")
    @property
    def allow_script(self) -> Optional[bool]:
        """
        Specifies whether a user can run scripts on the downloaded document.
        """
        return self.properties.get("AllowScript", None)

    @odata(name="AllowWriteCopy")
    @property
    def allow_write_copy(self) -> Optional[bool]:
        """
        Specifies whether a user can write in a copy of the downloaded document.
        """
        return self.properties.get("AllowWriteCopy", None)

    @odata(name="DisableDocumentBrowserView")
    @property
    def disable_document_browser_view(self) -> Optional[bool]:
        """Specifies whether a user can write in a copy of the downloaded document."""
        return self.properties.get("DisableDocumentBrowserView", None)

    @odata(name="DocumentAccessExpireDays")
    @property
    def document_access_expire_days(self) -> Optional[int]:
        """Specifies the number of days after which the downloaded document will expire."""
        return self.properties.get("DocumentAccessExpireDays", None)

    @odata(name="DocumentLibraryProtectionExpireDate")
    @property
    def document_library_protection_expire_date(self) -> Optional[datetime.datetime]:
        """
        Specifies the date on which the Information Rights Management (IRM) protection of this document library will
        stop.
        """
        return self.properties.get("DocumentLibraryProtectionExpireDate", datetime.datetime.min)

    @odata(name="EnableDocumentAccessExpire")
    @property
    def enable_document_access_expire(self) -> Optional[bool]:
        """Specifies whether the downloaded document will expire."""
        return self.properties.get("EnableDocumentAccessExpire", None)

    @odata(name="EnableGroupProtection")
    @property
    def enable_group_protection(self) -> Optional[bool]:
        """Specifies whether the permission of the downloaded document is applicable to a group."""
        return self.properties.get("EnableGroupProtection", None)

    @odata(name="EnableLicenseCacheExpire")
    @property
    def enable_license_cache_expire(self) -> Optional[int]:
        """Specifies whether a user MUST verify his or her credentials after certain intervals."""
        return self.properties.get("EnableLicenseCacheExpire", None)

    @odata(name="PolicyTitle")
    @property
    def policy_title(self) -> Optional[str]:
        """Specifies the permission policy title."""
        return self.properties.get("PolicyTitle", None)

    @odata(name="PolicyDescription")
    @property
    def policy_description(self) -> Optional[str]:
        """Specifies the permission policy description."""
        return self.properties.get("PolicyDescription", None)

    @odata(name="GroupName")
    @property
    def group_name(self) -> Optional[str]:
        """Specifies the group name (email address) that the permission is also applicable to."""
        return self.properties.get("GroupName", None)

    @odata(name="LicenseCacheExpireDays")
    @property
    def license_cache_expire_days(self) -> Optional[int]:
        """
        Specifies the number of days that the Information Rights Management (IRM) license can be cached by the
        application to open the downloaded document. When these elapse, the application will connect to the IRM
        server to validate the license.
        """
        return self.properties.get("LicenseCacheExpireDays", None)

    @odata(name="TemplateId")
    @property
    def template_id(self) -> Optional[str]:
        """Gets or sets the ID of the RMS template that will be applied to the file or library."""
        return self.properties.get("TemplateId", None)

    @odata(name="EnableDocumentBrowserPublishingView")
    @property
    def enable_document_browser_publishing_view(self) -> Optional[bool]:
        """Gets the EnableDocumentBrowserPublishingView property"""
        return self.properties.get("EnableDocumentBrowserPublishingView", None)

    def reset(self) -> Self:
        """Reset operation."""
        qry = ServiceOperationQuery(self, "Reset", None, {}, None, None)
        self.context.add_query(qry)
        return self
