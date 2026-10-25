from __future__ import annotations

from typing import Optional

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.documents.countbydate import CountByDate
from office365.sharepoint.entity import Entity


class RecentList(Entity):
    @odata(name="color")
    @property
    def color(self) -> Optional[str]:
        """Gets the color property"""
        return self.properties.get("color", None)

    @odata(name="createdByName")
    @property
    def created_by_name(self) -> Optional[str]:
        """Gets the createdByName property"""
        return self.properties.get("createdByName", None)

    @odata(name="createdByUpn")
    @property
    def created_by_upn(self) -> Optional[str]:
        """Gets the createdByUpn property"""
        return self.properties.get("createdByUpn", None)

    @odata(name="createdDate")
    @property
    def created_date(self) -> Optional[str]:
        """Gets the createdDate property"""
        return self.properties.get("createdDate", None)

    @odata(name="icon")
    @property
    def icon(self) -> Optional[str]:
        """Gets the icon property"""
        return self.properties.get("icon", None)

    @odata(name="lastModifiedDate")
    @property
    def last_modified_date(self) -> Optional[str]:
        """Gets the lastModifiedDate property"""
        return self.properties.get("lastModifiedDate", None)

    @odata(name="lastViewDate")
    @property
    def last_view_date(self) -> Optional[int]:
        """Gets the lastViewDate property"""
        return self.properties.get("lastViewDate", None)

    @odata(name="lastviewDateTime")
    @property
    def lastview_date_time(self) -> Optional[str]:
        """Gets the lastviewDateTime property"""
        return self.properties.get("lastviewDateTime", None)

    @odata(name="listId")
    @property
    def list_id(self) -> Optional[str]:
        """Gets the listId property"""
        return self.properties.get("listId", None)

    @odata(name="listTitle")
    @property
    def list_title(self) -> Optional[str]:
        """Gets the listTitle property"""
        return self.properties.get("listTitle", None)

    @odata(name="listUrl")
    @property
    def list_url(self) -> Optional[str]:
        """Gets the listUrl property"""
        return self.properties.get("listUrl", None)

    @odata(name="listViewCounts")
    @property
    def list_view_counts(self) -> ClientValueCollection[CountByDate]:
        """Gets the listViewCounts property"""
        return self.properties.get("listViewCounts", ClientValueCollection(CountByDate))

    @odata(name="shouldRemove")
    @property
    def should_remove(self) -> Optional[bool]:
        """Gets the shouldRemove property"""
        return self.properties.get("shouldRemove", None)

    @odata(name="siteColor")
    @property
    def site_color(self) -> Optional[str]:
        """Gets the siteColor property"""
        return self.properties.get("siteColor", None)

    @odata(name="siteId")
    @property
    def site_id(self) -> Optional[str]:
        """Gets the siteId property"""
        return self.properties.get("siteId", None)

    @odata(name="siteTitle")
    @property
    def site_title(self) -> Optional[str]:
        """Gets the siteTitle property"""
        return self.properties.get("siteTitle", None)

    @odata(name="siteUrl")
    @property
    def site_url(self) -> Optional[str]:
        """Gets the siteUrl property"""
        return self.properties.get("siteUrl", None)

    @odata(name="templateTypeId")
    @property
    def template_type_id(self) -> Optional[str]:
        """Gets the templateTypeId property"""
        return self.properties.get("templateTypeId", None)

    @odata(name="webId")
    @property
    def web_id(self) -> Optional[str]:
        """Gets the webId property"""
        return self.properties.get("webId", None)

    @odata(name="webTemplateConfiguration")
    @property
    def web_template_configuration(self) -> Optional[str]:
        """Gets the webTemplateConfiguration property"""
        return self.properties.get("webTemplateConfiguration", None)

    @odata(name="lastviewDateTime")
    @property
    def lastview_datetime(self) -> Optional[str]:
        """Gets the lastviewDateTime property"""
        return self.properties.get("lastviewDateTime", None)
