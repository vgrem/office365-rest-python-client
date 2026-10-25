from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.fields.multi_choice import FieldMultiChoice


class FieldRatingScale(FieldMultiChoice):
    """Specifies a field (2) that contains rating scale values for a survey list.
    To set properties, call the Update method (section 3.2.5.54.2.1.5)."""

    @odata(name="GridStartNumber")
    @property
    def grid_start_number(self) -> Optional[int]:
        """Gets the start number for the rating scale."""
        return self.properties.get("GridStartNumber", None)

    @grid_start_number.setter
    def grid_start_number(self, value: int) -> None:
        """Gets the start number for the rating scale."""
        self.set_property("GridStartNumber", value)

    @odata(name="RangeCount")
    @property
    def range_count(self) -> Optional[int]:
        """Specifies the number of options in the rating scale."""
        return self.properties.get("RangeCount", None)

    @odata(name="GridEndNumber")
    @property
    def grid_end_number(self) -> Optional[int]:
        """Gets the GridEndNumber property"""
        return self.properties.get("GridEndNumber", None)

    @odata(name="GridNAOptionText")
    @property
    def grid_na_option_text(self) -> Optional[str]:
        """Gets the GridNAOptionText property"""
        return self.properties.get("GridNAOptionText", None)

    @odata(name="GridTextRangeAverage")
    @property
    def grid_text_range_average(self) -> Optional[str]:
        """Gets the GridTextRangeAverage property"""
        return self.properties.get("GridTextRangeAverage", None)

    @odata(name="GridTextRangeHigh")
    @property
    def grid_text_range_high(self) -> Optional[str]:
        """Gets the GridTextRangeHigh property"""
        return self.properties.get("GridTextRangeHigh", None)

    @odata(name="GridTextRangeLow")
    @property
    def grid_text_range_low(self) -> Optional[str]:
        """Gets the GridTextRangeLow property"""
        return self.properties.get("GridTextRangeLow", None)
