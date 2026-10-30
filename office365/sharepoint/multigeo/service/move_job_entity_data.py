from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class MoveJobEntityData(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.MoveJobEntityData"

    @odata(name="ApiVersion")
    @property
    def api_version(self) -> Optional[str]:
        """Gets the ApiVersion property"""
        return self.properties.get("ApiVersion", None)

    @odata(name="BatchId", beta=True)
    @property
    def batch_id(self) -> Optional[UUID]:
        """Gets the BatchId property"""
        return self.properties.get("BatchId", None)

    @odata(name="CancelTriggeredBy")
    @property
    def cancel_triggered_by(self) -> Optional[str]:
        """Gets the CancelTriggeredBy property"""
        return self.properties.get("CancelTriggeredBy", None)

    @odata(name="DestinationDataLocation")
    @property
    def destination_data_location(self) -> Optional[str]:
        """Gets the DestinationDataLocation property"""
        return self.properties.get("DestinationDataLocation", None)

    @odata(name="Direction")
    @property
    def direction(self) -> Optional[int]:
        """Gets the Direction property"""
        return self.properties.get("Direction", None)

    @odata(name="ErrorMessage")
    @property
    def error_message(self) -> Optional[str]:
        """Gets the ErrorMessage property"""
        return self.properties.get("ErrorMessage", None)

    @odata(name="FinishedDateInUtc")
    @property
    def finished_date_in_utc(self) -> Optional[datetime]:
        """Gets the FinishedDateInUtc property"""
        return self.properties.get("FinishedDateInUtc", datetime.min)

    @odata(name="Id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    @odata(name="IsReadOnlyAlertRaised")
    @property
    def is_read_only_alert_raised(self) -> Optional[bool]:
        """Gets the IsReadOnlyAlertRaised property"""
        return self.properties.get("IsReadOnlyAlertRaised", None)

    @odata(name="JobPhase")
    @property
    def job_phase(self) -> Optional[int]:
        """Gets the JobPhase property"""
        return self.properties.get("JobPhase", None)

    @odata(name="Notify")
    @property
    def notify(self) -> Optional[str]:
        """Gets the Notify property"""
        return self.properties.get("Notify", None)

    @odata(name="Option")
    @property
    def option(self) -> Optional[int]:
        """Gets the Option property"""
        return self.properties.get("Option", None)

    @odata(name="PreferredMoveBeginDateInUtc")
    @property
    def preferred_move_begin_date_in_utc(self) -> Optional[datetime]:
        """Gets the PreferredMoveBeginDateInUtc property"""
        return self.properties.get("PreferredMoveBeginDateInUtc", datetime.min)

    @odata(name="PreferredMoveEndDateInUtc")
    @property
    def preferred_move_end_date_in_utc(self) -> Optional[datetime]:
        """Gets the PreferredMoveEndDateInUtc property"""
        return self.properties.get("PreferredMoveEndDateInUtc", datetime.min)

    @odata(name="Reserve")
    @property
    def reserve(self) -> Optional[str]:
        """Gets the Reserve property"""
        return self.properties.get("Reserve", None)

    @odata(name="SiteId")
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @odata(name="SourceDataLocation")
    @property
    def source_data_location(self) -> Optional[str]:
        """Gets the SourceDataLocation property"""
        return self.properties.get("SourceDataLocation", None)

    @odata(name="State")
    @property
    def state(self) -> Optional[int]:
        """Gets the State property"""
        return self.properties.get("State", None)

    @odata(name="SubType")
    @property
    def sub_type(self) -> Optional[int]:
        """Gets the SubType property"""
        return self.properties.get("SubType", None)

    @odata(name="TriggeredBy")
    @property
    def triggered_by(self) -> Optional[str]:
        """Gets the TriggeredBy property"""
        return self.properties.get("TriggeredBy", None)

    @odata(name="Type")
    @property
    def type(self) -> Optional[int]:
        """Gets the Type property"""
        return self.properties.get("Type", None)
