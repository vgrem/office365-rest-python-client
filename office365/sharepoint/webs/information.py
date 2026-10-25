from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class WebInformation(Entity):
    """Specifies metadata about a site"""

    def __repr__(self):
        return self.server_relative_url or self.entity_type_name

    @odata(name="Configuration")
    @property
    def configuration(self) -> Optional[str]:
        """Specifies the identifier (ID) of the site definition configuration that was used to create the site"""
        return self.properties.get("Configuration", None)

    @odata(name="Created")
    @property
    def created(self) -> Optional[datetime]:
        """Specifies when the site (2) was created."""
        return self.properties.get("Created", datetime.min)

    @odata(name="Description")
    @property
    def description(self) -> Optional[str]:
        """Specifies the description for the site"""
        return self.properties.get("Description", None)

    @odata(name="Id")
    @property
    def id(self) -> Optional[str]:
        """Specifies the site identifier for the site"""
        return self.properties.get("Id", None)

    @odata(name="Language")
    @property
    def language(self) -> Optional[int]:
        """Specifies the language code identifier (LCID) for the language that is used on the site"""
        return self.properties.get("Language", None)

    @odata(name="LastItemModifiedDate")
    @property
    def last_item_modified_date(self) -> Optional[datetime]:
        """Gets the date and time that an item was last modified in the site by a non-system update.
        A non-system update is a change to a list item that is visible to end users."""
        return self.properties.get("LastItemModifiedDate", datetime.min)

    @odata(name="ServerRelativeUrl")
    @property
    def server_relative_url(self) -> Optional[str]:
        """Specifies the server-relative URL of the site"""
        return self.properties.get("ServerRelativeUrl", None)

    @odata(name="Title")
    @property
    def title(self) -> Optional[str]:
        """Specifies the title for the site. Its length MUST be equal to or less than 255."""
        return self.properties.get("Title", None)

    @odata(name="WebTemplate")
    @property
    def web_template(self) -> Optional[str]:
        """Specifies the name of the site template that was used to create the site."""
        return self.properties.get("WebTemplate", None)

    @odata(name="WebTemplateId")
    @property
    def web_template_id(self) -> Optional[int]:
        """Specifies the identifier of the site template that was used to create the site"""
        return self.properties.get("WebTemplateId", None)

    @odata(name="LastItemUserModifiedDate")
    @property
    def last_item_user_modified_date(self) -> Optional[datetime]:
        """Gets the LastItemUserModifiedDate property"""
        return self.properties.get("LastItemUserModifiedDate", datetime.min)
