from __future__ import annotations

from dataclasses import field

from office365.directory.policies.validating_domains import ValidatingDomains
from office365.runtime.types.collections import StringCollection


class EnumeratedDomains(ValidatingDomains):
    domainNames: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EnumeratedDomains"
