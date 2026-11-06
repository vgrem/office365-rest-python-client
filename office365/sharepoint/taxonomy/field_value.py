from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TaxonomyFieldValue(ClientValue):
    """Represents a single value held in a TaxonomyField (section 3.1.5.27) object.

    Args:
        label: Specifies the label of the TaxonomyField (section 3.1.5.27) object.
        term_guid: Specifies a string representing Term (section 3.1.5.16) GUID.
        wss_id: Specifies the list item identifier of the list item containing the TaxonomyFieldValue
            that is encapsulated by the TaxonomyFieldValue (section 3.1.5.13) object.
    """

    Label: str | None = None
    TermGuid: str | None = None
    WssId: int = -1

    def __str__(self):
        # The note text has no place for a missing part: a ``None`` label was written
        # to the column as the literal label "None" (``#None|guid`` on read-back).
        return f"{self.WssId};#{self.Label or ''}|{self.TermGuid or ''}"

    @property
    def entity_type_name(self) -> str:
        return "SP.Taxonomy.TaxonomyFieldValue"
