from __future__ import annotations

from typing import Optional

from office365.booking.mailbox_details import MailboxDetails
from office365.booking.place_mode import PlaceMode
from office365.booking.place_service_plan_info import PlaceServicePlanInfo
from office365.entity import Entity
from office365.outlook.place_feature_enablement import PlaceFeatureEnablement
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class Desk(Entity):
    @odata(name="displayDeviceName")
    @property
    def display_device_name(self) -> Optional[str]:
        """Gets the displayDeviceName property"""
        return self.properties.get("displayDeviceName", None)

    @odata(name="heightAdjustableState")
    @property
    def height_adjustable_state(self) -> PlaceFeatureEnablement:
        """Gets the heightAdjustableState property"""
        return self.properties.get("heightAdjustableState", PlaceFeatureEnablement.unknown)

    @odata(name="mailboxDetails")
    @property
    def mailbox_details(self) -> MailboxDetails:
        """Gets the mailboxDetails property"""
        return self.properties.get("mailboxDetails", MailboxDetails())

    @odata(name="mode")
    @property
    def mode(self) -> PlaceMode:
        """Gets the mode property"""
        return self.properties.get("mode", PlaceMode())

    @odata(name="servicePlans")
    @property
    def service_plans(self) -> ClientValueCollection[PlaceServicePlanInfo]:
        """Gets the servicePlans property"""
        return self.properties.get("servicePlans", ClientValueCollection[PlaceServicePlanInfo](PlaceServicePlanInfo))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Desk"
