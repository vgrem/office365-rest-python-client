from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.managed.windows.defender_product_status import (
        WindowsDefenderProductStatus,
    )
    from office365.intune.devices.management.managed.windows.healthstate import (
        WindowsDeviceHealthState,
    )
    from office365.intune.devices.management.windowsmalware.windows_device_malware_state import (
        WindowsDeviceMalwareState,
    )


class WindowsProtectionState(Entity):
    @odata(name="antiMalwareVersion")
    @property
    def anti_malware_version(self) -> Optional[str]:
        """Gets the antiMalwareVersion property"""
        return self.properties.get("antiMalwareVersion", None)

    @odata(name="controlledConfigurationEnabled")
    @property
    def controlled_configuration_enabled(self) -> Optional[bool]:
        """Gets the controlledConfigurationEnabled property"""
        return self.properties.get("controlledConfigurationEnabled", None)

    @odata(name="deviceState")
    @property
    def device_state(self) -> WindowsDeviceHealthState:
        """Gets the deviceState property"""
        from office365.intune.devices.management.managed.windows.healthstate import (
            WindowsDeviceHealthState,
        )

        return self.properties.get("deviceState", WindowsDeviceHealthState.clean)

    @odata(name="engineVersion")
    @property
    def engine_version(self) -> Optional[str]:
        """Gets the engineVersion property"""
        return self.properties.get("engineVersion", None)

    @odata(name="fullScanOverdue")
    @property
    def full_scan_overdue(self) -> Optional[bool]:
        """Gets the fullScanOverdue property"""
        return self.properties.get("fullScanOverdue", None)

    @odata(name="fullScanRequired")
    @property
    def full_scan_required(self) -> Optional[bool]:
        """Gets the fullScanRequired property"""
        return self.properties.get("fullScanRequired", None)

    @odata(name="isVirtualMachine")
    @property
    def is_virtual_machine(self) -> Optional[bool]:
        """Gets the isVirtualMachine property"""
        return self.properties.get("isVirtualMachine", None)

    @odata(name="lastFullScanDateTime")
    @property
    def last_full_scan_date_time(self) -> Optional[datetime]:
        """Gets the lastFullScanDateTime property"""
        return self.properties.get("lastFullScanDateTime", datetime.min)

    @odata(name="lastFullScanSignatureVersion")
    @property
    def last_full_scan_signature_version(self) -> Optional[str]:
        """Gets the lastFullScanSignatureVersion property"""
        return self.properties.get("lastFullScanSignatureVersion", None)

    @odata(name="lastQuickScanDateTime")
    @property
    def last_quick_scan_date_time(self) -> Optional[datetime]:
        """Gets the lastQuickScanDateTime property"""
        return self.properties.get("lastQuickScanDateTime", datetime.min)

    @odata(name="lastQuickScanSignatureVersion")
    @property
    def last_quick_scan_signature_version(self) -> Optional[str]:
        """Gets the lastQuickScanSignatureVersion property"""
        return self.properties.get("lastQuickScanSignatureVersion", None)

    @odata(name="lastReportedDateTime")
    @property
    def last_reported_date_time(self) -> Optional[datetime]:
        """Gets the lastReportedDateTime property"""
        return self.properties.get("lastReportedDateTime", datetime.min)

    @odata(name="malwareProtectionEnabled")
    @property
    def malware_protection_enabled(self) -> Optional[bool]:
        """Gets the malwareProtectionEnabled property"""
        return self.properties.get("malwareProtectionEnabled", None)

    @odata(name="networkInspectionSystemEnabled")
    @property
    def network_inspection_system_enabled(self) -> Optional[bool]:
        """Gets the networkInspectionSystemEnabled property"""
        return self.properties.get("networkInspectionSystemEnabled", None)

    @odata(name="productStatus")
    @property
    def product_status(self) -> WindowsDefenderProductStatus:
        """Gets the productStatus property"""
        from office365.intune.devices.management.managed.windows.defender_product_status import (
            WindowsDefenderProductStatus,
        )

        return self.properties.get("productStatus", WindowsDefenderProductStatus.noStatus)

    @odata(name="quickScanOverdue")
    @property
    def quick_scan_overdue(self) -> Optional[bool]:
        """Gets the quickScanOverdue property"""
        return self.properties.get("quickScanOverdue", None)

    @odata(name="realTimeProtectionEnabled")
    @property
    def real_time_protection_enabled(self) -> Optional[bool]:
        """Gets the realTimeProtectionEnabled property"""
        return self.properties.get("realTimeProtectionEnabled", None)

    @odata(name="rebootRequired")
    @property
    def reboot_required(self) -> Optional[bool]:
        """Gets the rebootRequired property"""
        return self.properties.get("rebootRequired", None)

    @odata(name="signatureUpdateOverdue")
    @property
    def signature_update_overdue(self) -> Optional[bool]:
        """Gets the signatureUpdateOverdue property"""
        return self.properties.get("signatureUpdateOverdue", None)

    @odata(name="signatureVersion")
    @property
    def signature_version(self) -> Optional[str]:
        """Gets the signatureVersion property"""
        return self.properties.get("signatureVersion", None)

    @odata(name="tamperProtectionEnabled")
    @property
    def tamper_protection_enabled(self) -> Optional[bool]:
        """Gets the tamperProtectionEnabled property"""
        return self.properties.get("tamperProtectionEnabled", None)

    @odata(name="detectedMalwareState", navigation=True)
    @property
    def detected_malware_state(self) -> EntityCollection[WindowsDeviceMalwareState]:
        """Gets the detectedMalwareState property"""
        from office365.intune.devices.management.windowsmalware.windows_device_malware_state import (
            WindowsDeviceMalwareState,
        )

        return self.properties.get(
            "detectedMalwareState",
            EntityCollection[WindowsDeviceMalwareState](
                self.context, WindowsDeviceMalwareState, ResourcePath("detectedMalwareState", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsProtectionState"
