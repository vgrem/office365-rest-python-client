from __future__ import annotations

from dataclasses import dataclass, field

from office365.copilot.package_element import PackageElement
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class PackageElementDetail(ClientValue):
    elements: ClientValueCollection[PackageElement] = field(
        default_factory=lambda: ClientValueCollection(PackageElement)
    )
    elementType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PackageElementDetail"
