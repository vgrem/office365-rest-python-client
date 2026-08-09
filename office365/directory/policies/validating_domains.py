from __future__ import annotations

from dataclasses import dataclass

from office365.directory.objects.root_domains import RootDomains
from office365.runtime.client_value import ClientValue


@dataclass
class ValidatingDomains(ClientValue):
    rootDomains: RootDomains = RootDomains.none

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ValidatingDomains"
