from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.fields.field import Field


class FieldCalculated(Field):
    """
    Specifies a calculated field in a list. To set properties, call the Update method (section 3.2.5.38.2.1.5).

    The NoCrawl and SchemaXmlWithResourceTokens properties are not included in the default scalar property set
        for this type.
    """

    @odata(name="CurrencyLocaleId")
    @property
    def currency_locale_id(self) -> Optional[int]:
        """Gets the locale ID that is used for currency on the Web site."""
        return self.properties.get("CurrencyLocaleId", None)

    @odata(name="Formula")
    @property
    def formula(self) -> Optional[str]:
        """Specifies the formula for the field"""
        return self.properties.get("Formula", None)

    @formula.setter
    def formula(self, val: str) -> None:
        """Sets a value that specifies the Formula."""
        self.set_property("Formula", val)

    @odata(name="DateFormat")
    @property
    def date_format(self) -> Optional[int]:
        """Gets the DateFormat property"""
        return self.properties.get("DateFormat", None)

    @odata(name="DisplayFormat")
    @property
    def display_format(self) -> Optional[int]:
        """Gets the DisplayFormat property"""
        return self.properties.get("DisplayFormat", None)

    @odata(name="OutputType")
    @property
    def output_type(self) -> Optional[int]:
        """Gets the OutputType property"""
        return self.properties.get("OutputType", None)

    @odata(name="ShowAsPercentage")
    @property
    def show_as_percentage(self) -> Optional[bool]:
        """Gets the ShowAsPercentage property"""
        return self.properties.get("ShowAsPercentage", None)
