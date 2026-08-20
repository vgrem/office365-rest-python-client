from __future__ import annotations

from dataclasses import dataclass

from office365.directory.extensions.custom.customextensionendpointconfiguration import (
    CustomExtensionEndpointConfiguration,
)


@dataclass
class HttpRequestEndpoint(CustomExtensionEndpointConfiguration):
    targetUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.HttpRequestEndpoint"
