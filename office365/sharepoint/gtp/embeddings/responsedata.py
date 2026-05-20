from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class GptEmbeddingsResponseData(ClientValue):
    Embedding: ClientValueCollection[float] = field(default_factory=lambda: ClientValueCollection(float))
    Index: Optional[int] = None
    Object: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptEmbeddingsResponseData"
