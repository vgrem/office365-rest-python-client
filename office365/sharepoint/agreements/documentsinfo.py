from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.document import AgreementDocument


class AgreementDocumentsInfo(ClientValue):
    Documents: ClientValueCollection[AgreementDocument] = field(
        default_factory=lambda: ClientValueCollection(AgreementDocument)
    )
