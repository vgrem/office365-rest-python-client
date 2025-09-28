from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.data_validation_failure import ListDataValidationFailure


class ListDataValidationExceptionValue(ClientValue):
    """Specifies failure information for a failed field or list item data validation."""

    def __init__(
        self,
        field_failures=None,
        item_failure: ListDataValidationFailure = ListDataValidationFailure(),
    ):
        self.FieldFailures = ClientValueCollection(
            ListDataValidationFailure, field_failures
        )
        self.ItemFailure = item_failure
