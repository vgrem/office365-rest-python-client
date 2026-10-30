from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.mobileapps.win32.lob_app_install_experience import (
        Win32LobAppInstallExperience,
    )
    from office365.intune.devices.management.mobileapps.win32.lob_app_msi_information import (
        Win32LobAppMsiInformation,
    )
    from office365.intune.devices.management.mobileapps.win32.lob_app_return_code import (
        Win32LobAppReturnCode,
    )
    from office365.intune.devices.management.mobileapps.win32.lob_app_rule import (
        Win32LobAppRule,
    )
    from office365.intune.devices.management.mobileapps.windows.architecture import (
        WindowsArchitecture,
    )


class Win32LobApp(Entity):
    @odata(name="allowedArchitectures")
    @property
    def allowed_architectures(self) -> WindowsArchitecture:
        """Gets the allowedArchitectures property"""
        from office365.intune.devices.management.mobileapps.windows.architecture import (
            WindowsArchitecture,
        )

        return self.properties.get("allowedArchitectures", WindowsArchitecture.none)

    @odata(name="applicableArchitectures")
    @property
    def applicable_architectures(self) -> WindowsArchitecture:
        """Gets the applicableArchitectures property"""
        from office365.intune.devices.management.mobileapps.windows.architecture import (
            WindowsArchitecture,
        )

        return self.properties.get("applicableArchitectures", WindowsArchitecture.none)

    @odata(name="installCommandLine")
    @property
    def install_command_line(self) -> Optional[str]:
        """Gets the installCommandLine property"""
        return self.properties.get("installCommandLine", None)

    @odata(name="installExperience")
    @property
    def install_experience(self) -> Optional[Win32LobAppInstallExperience]:
        """Gets the installExperience property"""
        return self.properties.get("installExperience", None)

    @odata(name="minimumCpuSpeedInMHz")
    @property
    def minimum_cpu_speed_in_mhz(self) -> Optional[int]:
        """Gets the minimumCpuSpeedInMHz property"""
        return self.properties.get("minimumCpuSpeedInMHz", None)

    @odata(name="minimumFreeDiskSpaceInMB")
    @property
    def minimum_free_disk_space_in_mb(self) -> Optional[int]:
        """Gets the minimumFreeDiskSpaceInMB property"""
        return self.properties.get("minimumFreeDiskSpaceInMB", None)

    @odata(name="minimumMemoryInMB")
    @property
    def minimum_memory_in_mb(self) -> Optional[int]:
        """Gets the minimumMemoryInMB property"""
        return self.properties.get("minimumMemoryInMB", None)

    @odata(name="minimumNumberOfProcessors")
    @property
    def minimum_number_of_processors(self) -> Optional[int]:
        """Gets the minimumNumberOfProcessors property"""
        return self.properties.get("minimumNumberOfProcessors", None)

    @odata(name="minimumSupportedWindowsRelease")
    @property
    def minimum_supported_windows_release(self) -> Optional[str]:
        """Gets the minimumSupportedWindowsRelease property"""
        return self.properties.get("minimumSupportedWindowsRelease", None)

    @odata(name="msiInformation")
    @property
    def msi_information(self) -> Optional[Win32LobAppMsiInformation]:
        """Gets the msiInformation property"""
        return self.properties.get("msiInformation", None)

    @odata(name="returnCodes")
    @property
    def return_codes(self) -> ClientValueCollection[Win32LobAppReturnCode]:
        """Gets the returnCodes property"""
        from office365.intune.devices.management.mobileapps.win32.lob_app_return_code import (
            Win32LobAppReturnCode,
        )

        return self.properties.get("returnCodes", ClientValueCollection[Win32LobAppReturnCode](Win32LobAppReturnCode))

    @odata(name="rules")
    @property
    def rules(self) -> ClientValueCollection[Win32LobAppRule]:
        """Gets the rules property"""
        from office365.intune.devices.management.mobileapps.win32.lob_app_rule import (
            Win32LobAppRule,
        )

        return self.properties.get("rules", ClientValueCollection[Win32LobAppRule](Win32LobAppRule))

    @odata(name="setupFilePath")
    @property
    def setup_file_path(self) -> Optional[str]:
        """Gets the setupFilePath property"""
        return self.properties.get("setupFilePath", None)

    @odata(name="uninstallCommandLine")
    @property
    def uninstall_command_line(self) -> Optional[str]:
        """Gets the uninstallCommandLine property"""
        return self.properties.get("uninstallCommandLine", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Win32LobApp"
