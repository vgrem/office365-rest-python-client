from __future__ import annotations

from office365.directory.applications.application import Application
from office365.entity_collection import EntityCollection
from office365.runtime.client_value import ClientValue


class CustomTaskExtensionCallbackConfiguration(ClientValue):
    authorizedApps: EntityCollection[Application] | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.CustomTaskExtensionCallbackConfiguration"
