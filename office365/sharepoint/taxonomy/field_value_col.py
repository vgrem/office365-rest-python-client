from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.taxonomy.field_value import TaxonomyFieldValue


class TaxonomyFieldValueCollection(ClientValueCollection[TaxonomyFieldValue]):
    """Represents the multi-value object for the taxonomy column."""

    def __init__(self, initial_values):
        """
        :param list[TaxonomyFieldValue] initial_values:
        """
        super().__init__(TaxonomyFieldValue, initial_values)

    def __str__(self):
        return ";#".join([str(item) for item in self._data])
