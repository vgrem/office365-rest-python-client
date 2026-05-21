from dataclasses import dataclass

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.taxonomy.field_value import TaxonomyFieldValue


@dataclass(init=False)
class TaxonomyFieldValueCollection(ClientValueCollection[TaxonomyFieldValue]):
    """Represents the multi-value object for the taxonomy column."""

    def __str__(self):
        return ";#".join([str(item) for item in self._data])
