from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SPMachineLearningWorkItem(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningWorkItem"

    @odata(name="Created", beta=True)
    @property
    def created(self) -> Optional[datetime]:
        """Gets the Created property"""
        return self.properties.get("Created", datetime.min)

    @odata(name="DeliverDate", beta=True)
    @property
    def deliver_date(self) -> Optional[datetime]:
        """Gets the DeliverDate property"""
        return self.properties.get("DeliverDate", datetime.min)

    @odata(name="ErrorMessage", beta=True)
    @property
    def error_message(self) -> Optional[str]:
        """Gets the ErrorMessage property"""
        return self.properties.get("ErrorMessage", None)

    @odata(name="ID", beta=True)
    @property
    def id_(self) -> Optional[UUID]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    @odata(name="Status", beta=True)
    @property
    def status(self) -> Optional[str]:
        """Gets the Status property"""
        return self.properties.get("Status", None)

    @odata(name="StatusCode", beta=True)
    @property
    def status_code(self) -> Optional[int]:
        """Gets the StatusCode property"""
        return self.properties.get("StatusCode", None)

    @odata(name="TargetServerRelativeUrl", beta=True)
    @property
    def target_server_relative_url(self) -> Optional[str]:
        """Gets the TargetServerRelativeUrl property"""
        return self.properties.get("TargetServerRelativeUrl", None)

    @odata(name="TargetSiteId", beta=True)
    @property
    def target_site_id(self) -> Optional[UUID]:
        """Gets the TargetSiteId property"""
        return self.properties.get("TargetSiteId", None)

    @odata(name="TargetSiteUrl", beta=True)
    @property
    def target_site_url(self) -> Optional[str]:
        """Gets the TargetSiteUrl property"""
        return self.properties.get("TargetSiteUrl", None)

    @odata(name="TargetUniqueId", beta=True)
    @property
    def target_unique_id(self) -> Optional[UUID]:
        """Gets the TargetUniqueId property"""
        return self.properties.get("TargetUniqueId", None)

    @odata(name="TargetWebId", beta=True)
    @property
    def target_web_id(self) -> Optional[UUID]:
        """Gets the TargetWebId property"""
        return self.properties.get("TargetWebId", None)

    @odata(name="TargetWebServerRelativeUrl", beta=True)
    @property
    def target_web_server_relative_url(self) -> Optional[str]:
        """Gets the TargetWebServerRelativeUrl property"""
        return self.properties.get("TargetWebServerRelativeUrl", None)

    @odata(name="Type", beta=True)
    @property
    def type_(self) -> Optional[UUID]:
        """Gets the Type property"""
        return self.properties.get("Type", None)

    @odata(name="ID", beta=True)
    @property
    def id(self) -> Optional[UUID]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    @odata(name="Type", beta=True)
    @property
    def type(self) -> Optional[UUID]:
        """Gets the Type property"""
        return self.properties.get("Type", None)
