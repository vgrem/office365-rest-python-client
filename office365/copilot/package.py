from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.copilot.copilot_package_request_status import (
        CopilotPackageRequestStatus,
    )
    from office365.copilot.copilot_package_request_type import CopilotPackageRequestType
    from office365.copilot.package_type import PackageType
    from office365.intune.devices.management.package_status import PackageStatus
    from office365.runtime.types.json import Json


class CopilotPackage(Entity):
    @odata(name="agentIdentityId")
    @property
    def agent_identity_id(self) -> Optional[str]:
        """Gets the agentIdentityId property"""
        return self.properties.get("agentIdentityId", None)

    @odata(name="appId")
    @property
    def app_id(self) -> Optional[str]:
        """Gets the appId property"""
        return self.properties.get("appId", None)

    @odata(name="assetId")
    @property
    def asset_id(self) -> Optional[str]:
        """Gets the assetId property"""
        return self.properties.get("assetId", None)

    @odata(name="availableTo")
    @property
    def available_to(self) -> PackageStatus:
        """Gets the availableTo property"""
        from office365.intune.devices.management.package_status import PackageStatus

        return self.properties.get("availableTo", PackageStatus.none)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="deployedTo")
    @property
    def deployed_to(self) -> PackageStatus:
        """Gets the deployedTo property"""
        from office365.intune.devices.management.package_status import PackageStatus

        return self.properties.get("deployedTo", PackageStatus.none)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="elementTypes")
    @property
    def element_types(self) -> StringCollection:
        """Gets the elementTypes property"""
        return self.properties.get("elementTypes", StringCollection())

    @odata(name="governanceMetadata")
    @property
    def governance_metadata(self) -> Json:
        """Gets the governanceMetadata property"""
        from office365.runtime.types.json import Json

        return self.properties.get("governanceMetadata", Json())

    @odata(name="isBlocked")
    @property
    def is_blocked(self) -> Optional[bool]:
        """Gets the isBlocked property"""
        return self.properties.get("isBlocked", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="manifestId")
    @property
    def manifest_id(self) -> Optional[str]:
        """Gets the manifestId property"""
        return self.properties.get("manifestId", None)

    @odata(name="manifestVersion")
    @property
    def manifest_version(self) -> Optional[str]:
        """Gets the manifestVersion property"""
        return self.properties.get("manifestVersion", None)

    @odata(name="ownerId")
    @property
    def owner_id(self) -> Optional[str]:
        """Gets the ownerId property"""
        return self.properties.get("ownerId", None)

    @odata(name="platform")
    @property
    def platform(self) -> Optional[str]:
        """Gets the platform property"""
        return self.properties.get("platform", None)

    @odata(name="publisher")
    @property
    def publisher(self) -> Optional[str]:
        """Gets the publisher property"""
        return self.properties.get("publisher", None)

    @odata(name="requestStatus")
    @property
    def request_status(self) -> CopilotPackageRequestStatus:
        """Gets the requestStatus property"""
        from office365.copilot.copilot_package_request_status import (
            CopilotPackageRequestStatus,
        )

        return self.properties.get("requestStatus", CopilotPackageRequestStatus.pending)

    @odata(name="requestType")
    @property
    def request_type(self) -> CopilotPackageRequestType:
        """Gets the requestType property"""
        from office365.copilot.copilot_package_request_type import (
            CopilotPackageRequestType,
        )

        return self.properties.get("requestType", CopilotPackageRequestType.publish)

    @odata(name="shortDescription")
    @property
    def short_description(self) -> Optional[str]:
        """Gets the shortDescription property"""
        return self.properties.get("shortDescription", None)

    @odata(name="supportedHosts")
    @property
    def supported_hosts(self) -> StringCollection:
        """Gets the supportedHosts property"""
        return self.properties.get("supportedHosts", StringCollection())

    @odata(name="type")
    @property
    def type(self) -> PackageType:
        """Gets the type property"""
        from office365.copilot.package_type import PackageType

        return self.properties.get("type", PackageType.microsoft)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @odata(name="zipFile")
    @property
    def zip_file(self) -> Optional[bytes]:
        """Gets the zipFile property"""
        return self.properties.get("zipFile", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CopilotPackage"
