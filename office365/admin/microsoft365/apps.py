from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.admin.microsoft365.m365_apps_installation_options import (
        M365AppsInstallationOptions,
    )


class AdminMicrosoft365Apps(Entity):
    """Represents an entity that acts as a container for administrator functionality for Microsoft 365 applications."""

    @odata(name="installationOptions", navigation=True)
    @property
    def installation_options(self) -> M365AppsInstallationOptions:
        """Gets the installationOptions property"""
        from office365.admin.microsoft365.m365_apps_installation_options import (
            M365AppsInstallationOptions,
        )

        return self.properties.get(
            "installationOptions",
            M365AppsInstallationOptions(self.context, ResourcePath("installationOptions", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AdminMicrosoft365Apps"
