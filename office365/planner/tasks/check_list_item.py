from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class PlannerChecklistItem(ClientValue):
    """
    The plannerChecklistItem resource represents an item in the checklist of a task.
    The checklist on a task is represented by the checklistItems object.

    :param str|None title: The title of the checklist.
    """

    title: str | None = None
