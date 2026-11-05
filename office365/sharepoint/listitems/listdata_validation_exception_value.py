from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.data_validation_failure import ListDataValidationFailure


class ListDataValidationExceptionValue(ClientValue):
    """
    Specifies failure information for a failed field or list item data validation.
    """

    FieldFailures: ClientValueCollection[ListDataValidationFailure] = field(
        default_factory=lambda: ClientValueCollection(ListDataValidationFailure)
    )
    ItemFailure: ListDataValidationFailure = field(default_factory=ListDataValidationFailure)
