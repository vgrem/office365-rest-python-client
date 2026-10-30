from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.attendance_interval import AttendanceInterval
    from office365.communications.virtualevents.external_registration_information import (
        VirtualEventExternalRegistrationInformation,
    )
    from office365.directory.permissions.identity import Identity


class AttendanceRecord(Entity):
    @odata(name="attendanceIntervals")
    @property
    def attendance_intervals(self) -> ClientValueCollection[AttendanceInterval]:
        """Gets the attendanceIntervals property"""
        from office365.communications.attendance_interval import AttendanceInterval

        return self.properties.get("attendanceIntervals", ClientValueCollection[AttendanceInterval](AttendanceInterval))

    @odata(name="emailAddress")
    @property
    def email_address(self) -> Optional[str]:
        """Gets the emailAddress property"""
        return self.properties.get("emailAddress", None)

    @odata(name="externalRegistrationInformation")
    @property
    def external_registration_information(self) -> VirtualEventExternalRegistrationInformation:
        """Gets the externalRegistrationInformation property"""
        from office365.communications.virtualevents.external_registration_information import (
            VirtualEventExternalRegistrationInformation,
        )

        return self.properties.get("externalRegistrationInformation", VirtualEventExternalRegistrationInformation())

    @odata(name="identity")
    @property
    def identity(self) -> Identity:
        """Gets the identity property"""
        from office365.directory.permissions.identity import Identity

        return self.properties.get("identity", Identity())

    @odata(name="registrationId")
    @property
    def registration_id(self) -> Optional[str]:
        """Gets the registrationId property"""
        return self.properties.get("registrationId", None)

    @odata(name="role")
    @property
    def role(self) -> Optional[str]:
        """Gets the role property"""
        return self.properties.get("role", None)

    @odata(name="totalAttendanceInSeconds")
    @property
    def total_attendance_in_seconds(self) -> Optional[int]:
        """Gets the totalAttendanceInSeconds property"""
        return self.properties.get("totalAttendanceInSeconds", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AttendanceRecord"
