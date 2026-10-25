from __future__ import annotations

from typing import Optional

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.migrationcenter.folderinformation import SPFolderInformation


class ChannelResource(Entity):
    """"""

    @odata(name="AbsoluteUrl")
    @property
    def absolute_url(self) -> Optional[str]:
        """Gets the AbsoluteUrl property"""
        return self.properties.get("AbsoluteUrl", None)

    @odata(name="Description")
    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @odata(name="DisplayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the DisplayName property"""
        return self.properties.get("DisplayName", None)

    @odata(name="MembershipType")
    @property
    def membership_type(self) -> Optional[str]:
        """Gets the MembershipType property"""
        return self.properties.get("MembershipType", None)

    @odata(name="ServerRelativeUrl")
    @property
    def server_relative_url(self) -> Optional[str]:
        """Gets the ServerRelativeUrl property"""
        return self.properties.get("ServerRelativeUrl", None)

    @odata(name="SubFolders")
    @property
    def sub_folders(self) -> ClientValueCollection[SPFolderInformation]:
        """Gets the SubFolders property"""
        return self.properties.get("SubFolders", ClientValueCollection(SPFolderInformation))

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.Teams.ChannelResource"

    @odata(name="Id")
    @property
    def id(self) -> Optional[str]:
        """Gets the Id property"""
        return self.properties.get("Id", None)
