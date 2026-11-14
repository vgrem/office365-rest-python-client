from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.odata_property import odata


class DeviceAndAppManagementAssignmentTarget(ClientValue):
    """Who an assignment aims at.

    The service sends one of several shapes under this one name - ``allDevicesAssignmentTarget``,
    ``allLicensedUsersAssignmentTarget``, ``groupAssignmentTarget``,
    ``exclusionGroupAssignmentTarget`` - and only a group target carries a ``groupId``, so which
    target a policy reaches is read from ``group_id`` being set, not from a type name the payload
    does not spell. A filter, when there is one, narrows the target on both sides.

    https://learn.microsoft.com/en-us/graph/api/resources/deviceandappmanagementassignmenttarget
    """

    device_and_app_management_assignment_filter_id: Optional[str] = field(
        default=None, metadata=odata(name="deviceAndAppManagementAssignmentFilterId")
    )
    device_and_app_management_assignment_filter_type: Optional[str] = field(
        default=None, metadata=odata(name="deviceAndAppManagementAssignmentFilterType")
    )
    group_id: Optional[str] = field(default=None, metadata=odata(name="groupId"))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.deviceAndAppManagementAssignmentTarget"

    def __repr__(self) -> str:
        return self.group_id or "all devices and users"
