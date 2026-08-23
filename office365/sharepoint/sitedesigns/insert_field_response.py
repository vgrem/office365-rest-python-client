from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.field_item_insertion_details import FieldItemInsertionDetails


class InsertFieldResponse(ClientValue):
    FailedInsertions: ClientValueCollection[FieldItemInsertionDetails] = field(
        default_factory=lambda: ClientValueCollection(FieldItemInsertionDetails)
    )
    SuccessfulInsertions: ClientValueCollection[FieldItemInsertionDetails] = field(
        default_factory=lambda: ClientValueCollection(FieldItemInsertionDetails)
    )
