from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class MicrofeedPostDefinitionNames(ClientValue):
    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedPostDefinitionNames"
