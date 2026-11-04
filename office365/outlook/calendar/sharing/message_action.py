from __future__ import annotations

from office365.outlook.calendar.sharing.actionimportance import CalendarSharingActionImportance
from office365.outlook.calendar.sharing.actiontype import CalendarSharingActionType
from office365.outlook.calendar.sharing.types import CalendarSharingAction
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CalendarSharingMessageAction(ClientValue):
    action: CalendarSharingAction = CalendarSharingAction.accept
    actionType: CalendarSharingActionType = CalendarSharingActionType.accept
    importance: CalendarSharingActionImportance = CalendarSharingActionImportance.primary
    "Represents a calendar sharing message action."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CalendarSharingMessageAction"
