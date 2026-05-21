from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.translation.requested_translation import RequestedTranslation


@dataclass
class TranslationStatusSetRequest(ClientValue):
    RequestedTranslations: ClientValueCollection[RequestedTranslation] = field(
        default_factory=lambda: ClientValueCollection(RequestedTranslation)
    )
