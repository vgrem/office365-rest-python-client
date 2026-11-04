from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.translation.requested_translation import RequestedTranslation


@value
class TranslationStatusSetRequest(ClientValue):
    RequestedTranslations: ClientValueCollection[RequestedTranslation] = field(
        default_factory=lambda: ClientValueCollection(RequestedTranslation)
    )
