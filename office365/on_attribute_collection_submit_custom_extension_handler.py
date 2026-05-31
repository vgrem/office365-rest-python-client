from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.paths.resource_path import ResourcePath
from dataclasses import dataclass, field

@dataclass
class OnAttributeCollectionSubmitCustomExtensionHandler(ClientValue):
    configuration: CustomExtensionOverwriteConfiguration = field(default_factory=CustomExtensionOverwriteConfiguration)
    customExtension: OnAttributeCollectionSubmitCustomExtension | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.OnAttributeCollectionSubmitCustomExtensionHandler'