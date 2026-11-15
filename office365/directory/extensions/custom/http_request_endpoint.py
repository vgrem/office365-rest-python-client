from __future__ import annotations

from office365.directory.extensions.custom.extension_endpoint_configuration import (
    CustomExtensionEndpointConfiguration,
)


class HttpRequestEndpoint(CustomExtensionEndpointConfiguration):
    targetUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.HttpRequestEndpoint"
