"""Registered generation services: metadata reader + optional documentation provider.

Adding a service is a single registration here (or in a product module that
imports this one); the CLI and pipeline only look services up by name.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from generator.documentation.graph import GraphDocumentation
from generator.odata.v3.metadata_reader import ODataV3Reader
from generator.odata.v4.metadata_reader import ODataV4Reader


@dataclass(frozen=True)
class ServiceDefinition:
    """A model the generator can produce."""

    reader: type
    documentation: Optional[type] = None


SERVICES: dict[str, ServiceDefinition] = {
    # SharePoint metadata has no description source yet.
    "sharepoint": ServiceDefinition(ODataV3Reader),
    "graph": ServiceDefinition(ODataV4Reader, GraphDocumentation),
}


def get_service(name: str) -> ServiceDefinition:
    """The registered definition for ``name``."""
    return SERVICES[name]


def service_names() -> list[str]:
    """All registered service names (sorted)."""
    return sorted(SERVICES)
