from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.ui.applicationpages.peoplepicker.query_settings import (
    PeoplePickerQuerySettings,
)


class PickerSettings(Entity):
    """
    This class contains configuration settings for the client people picker control hosted
    by the SharePoint sharing UI.
    """

    @odata(name="AllowEmailAddresses")
    @property
    def allow_email_addresses(self) -> bool:
        """
        Boolean value indicating whether the picker control will allow the resolution of arbitrary email addresses.
        """
        return self.properties.get("AllowEmailAddresses", None)

    @odata(name="AllowOnlyEmailAddresses")
    @property
    def allow_only_email_addresses(self) -> bool:
        """
        Boolean value indicating whether the picker control will only allow the resolution of email addresses.
        """
        return self.properties.get("AllowOnlyEmailAddresses", None)

    @odata(name="QuerySettings")
    @property
    def query_settings(self) -> PeoplePickerQuerySettings:
        """
        The query settings to be used by the picker control.
        """
        return self.properties.get("QuerySettings", PeoplePickerQuerySettings())

    @odata(name="PrincipalAccountType")
    @property
    def principal_account_type(self) -> Optional[str]:
        """Gets the PrincipalAccountType property"""
        return self.properties.get("PrincipalAccountType", None)

    @odata(name="PrincipalSource")
    @property
    def principal_source(self) -> Optional[int]:
        """Gets the PrincipalSource property"""
        return self.properties.get("PrincipalSource", None)

    @odata(name="UseSubstrateSearch")
    @property
    def use_substrate_search(self) -> Optional[bool]:
        """Gets the UseSubstrateSearch property"""
        return self.properties.get("UseSubstrateSearch", None)

    @odata(name="VisibleSuggestions")
    @property
    def visible_suggestions(self) -> Optional[int]:
        """Gets the VisibleSuggestions property"""
        return self.properties.get("VisibleSuggestions", None)
