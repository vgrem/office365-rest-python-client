from __future__ import annotations

import json

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class LocalizedName(ClientValue):
    """
    Represents the localized name used in the term store, which identifies the name in the localized language.
    For more information, see localizedLabel.

    Sentinel for a payload: no OData type name is declared. The term store is served by
    SharePoint's own model, and it refuses a cast in the payload ("[termSetModel] The
    specified type named microsoft.graph.termStore.localizedName is not recognized"), in
    either case and with or without the leading ``#``; the plain object is accepted.
    """

    name: str | None = None
    languageTag: str = "en-US"

    def __repr__(self):
        return json.dumps(self.to_json())
