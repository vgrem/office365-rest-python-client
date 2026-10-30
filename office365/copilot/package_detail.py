from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.copilot.package_request_metadata import CopilotPackageRequestMetadata
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.copilot.package_access_entity import PackageAccessEntity
    from office365.copilot.package_element_detail import PackageElementDetail


class CopilotPackageDetail(Entity):
    @odata(name="acquireUsersAndGroups")
    @property
    def acquire_users_and_groups(self) -> ClientValueCollection[PackageAccessEntity]:
        """Gets the acquireUsersAndGroups property"""
        from office365.copilot.package_access_entity import PackageAccessEntity

        return self.properties.get(
            "acquireUsersAndGroups", ClientValueCollection[PackageAccessEntity](PackageAccessEntity)
        )

    @odata(name="activeUsers")
    @property
    def active_users(self) -> Optional[int]:
        """Gets the activeUsers property"""
        return self.properties.get("activeUsers", None)

    @odata(name="allowedUsersAndGroups")
    @property
    def allowed_users_and_groups(self) -> ClientValueCollection[PackageAccessEntity]:
        """Gets the allowedUsersAndGroups property"""
        from office365.copilot.package_access_entity import PackageAccessEntity

        return self.properties.get(
            "allowedUsersAndGroups", ClientValueCollection[PackageAccessEntity](PackageAccessEntity)
        )

    @odata(name="categories")
    @property
    def categories(self) -> StringCollection:
        """Gets the categories property"""
        return self.properties.get("categories", StringCollection())

    @odata(name="elementDetails")
    @property
    def element_details(self) -> ClientValueCollection[PackageElementDetail]:
        """Gets the elementDetails property"""
        from office365.copilot.package_element_detail import PackageElementDetail

        return self.properties.get("elementDetails", ClientValueCollection[PackageElementDetail](PackageElementDetail))

    @odata(name="exceptionRate")
    @property
    def exception_rate(self) -> Optional[float]:
        """Gets the exceptionRate property"""
        return self.properties.get("exceptionRate", None)

    @odata(name="lastUsedDateTime")
    @property
    def last_used_date_time(self) -> Optional[datetime]:
        """Gets the lastUsedDateTime property"""
        return self.properties.get("lastUsedDateTime", datetime.min)

    @odata(name="longDescription")
    @property
    def long_description(self) -> Optional[str]:
        """Gets the longDescription property"""
        return self.properties.get("longDescription", None)

    @odata(name="sensitivity")
    @property
    def sensitivity(self) -> Optional[str]:
        """Gets the sensitivity property"""
        return self.properties.get("sensitivity", None)

    @odata(name="sharedWithUsersAndGroups")
    @property
    def shared_with_users_and_groups(self) -> ClientValueCollection[PackageAccessEntity]:
        """Gets the sharedWithUsersAndGroups property"""
        from office365.copilot.package_access_entity import PackageAccessEntity

        return self.properties.get(
            "sharedWithUsersAndGroups", ClientValueCollection[PackageAccessEntity](PackageAccessEntity)
        )

    @odata(name="totalRunTimeInHours")
    @property
    def total_run_time_in_hours(self) -> Optional[float]:
        """Gets the totalRunTimeInHours property"""
        return self.properties.get("totalRunTimeInHours", None)

    @odata(name="totalSessions")
    @property
    def total_sessions(self) -> Optional[int]:
        """Gets the totalSessions property"""
        return self.properties.get("totalSessions", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CopilotPackageDetail"

    @odata(name="requestMetadata", readonly=True)
    @property
    def request_metadata(self) -> Optional[CopilotPackageRequestMetadata]:
        """Gets the requestMetadata property"""
        return self.properties.get("requestMetadata", None)
