from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class Windows10EnrollmentCompletionPageConfiguration(Entity):
    @odata(name="allowNonBlockingAppInstallation")
    @property
    def allow_non_blocking_app_installation(self) -> Optional[bool]:
        """Gets the allowNonBlockingAppInstallation property"""
        return self.properties.get("allowNonBlockingAppInstallation", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Windows10EnrollmentCompletionPageConfiguration"
