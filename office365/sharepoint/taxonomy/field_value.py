from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class TaxonomyFieldValue(ClientValue):
    """Represents a single value held in a TaxonomyField (section 3.1.5.27) object.

    :param str label: Specifies the label of the TaxonomyField (section 3.1.5.27) object.
    :parm str term_guid: Specifies a string representing Term (section 3.1.5.16) GUID.
    :parm int wss_id: Specifies the list item identifier of the list item containing the TaxonomyFieldValue
        that is encapsulated by the TaxonomyFieldValue (section 3.1.5.13) object.
    """

    Label: Optional[str] = None
    TermGuid: Optional[str] = None
    WssId: int = -1

    def __str__(self):
        return f"{self.WssId};#{self.Label}|{self.TermGuid}"

    @property
    def entity_type_name(self):
        return "SP.Taxonomy.TaxonomyFieldValue"
