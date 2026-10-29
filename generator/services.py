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
    #: The key a type inherits when the CSDL declares none. ``entity`` (Graph) spells it
    #: ``id``, ``SP.Entity`` (SharePoint) ``Id``; a derived type inherits its base's key,
    #: which is why the snapshots leave ``<Key>`` off the overwhelming majority of types,
    #: and why a derivation that lands on this spelling is no marker at all.
    default_key: str = "id"
    #: The sub-package of ``output_path`` that holds this service's own classes, when it
    #: has one. Graph's classes are spread over the whole package (``outlook``,
    #: ``directory``, ``intune``, ...), so the search stays tree-wide there; SharePoint's
    #: are all under ``sharepoint/``, and narrowing the search to them is what lets an
    #: ``SP.Attachment`` resolve to the SharePoint ``Attachment`` rather than being refused
    #: for a name three other namespaces reuse.
    model_package: str = ""
    #: Whether the CSDL's ``<Key>`` may be *written* into the model, or only reported.
    #: SharePoint's is not authoritative: it states a key on 613 of 871 entity types and
    #: states ones no client can address an entity by (``Alert`` by ``AlertFrequency``,
    #: ``ApiMetadata`` by a mangled ``Id4a81de...``). The 17 hand-written
    #: ``property_ref_name`` overrides there are the reviewed answer.
    keys_authoritative: bool = True


SERVICES: dict[str, ServiceDefinition] = {
    # SharePoint metadata has no description source yet.
    "sharepoint": ServiceDefinition(
        ODataV3Reader, default_key="Id", model_package="sharepoint", keys_authoritative=False
    ),
    "graph": ServiceDefinition(ODataV4Reader, GraphDocumentation),
}


def get_service(name: str) -> ServiceDefinition:
    """The registered definition for ``name``."""
    return SERVICES[name]


def service_names() -> list[str]:
    """All registered service names (sorted)."""
    return sorted(SERVICES)
