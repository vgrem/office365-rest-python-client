from __future__ import annotations


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.data_validation_failure import ListDataValidationFailure


@dataclass
class ListDataValidationExceptionValue(ClientValue):

    """
    Specifies failure information for a failed field or list item data validation.
    """

    FieldFailures: ClientValueCollection[ListDataValidationFailure] | None = None
    ItemFailure: ListDataValidationFailure = ListDataValidationFailure()