from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MicrofeedPostDefinitionNames(ClientValue):
    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedPostDefinitionNames"
