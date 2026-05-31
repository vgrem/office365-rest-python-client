from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from office365.runtime.paths.resource_path import ResourcePath
from typing import Optional

@dataclass
class OnPasswordMigrationCustomExtensionHandler(ClientValue):
    configuration: CustomExtensionOverwriteConfiguration = field(default_factory=CustomExtensionOverwriteConfiguration)
    migrationPropertyId: str | None = None
    customExtension: OnPasswordSubmitCustomExtension | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.OnPasswordMigrationCustomExtensionHandler'