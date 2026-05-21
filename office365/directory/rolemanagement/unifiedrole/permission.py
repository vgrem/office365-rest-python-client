from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class UnifiedRolePermission(ClientValue):
    """
    Represents a collection of allowed resource actions and the conditions that must be met for the action to be
    allowed. Resource actions are tasks that can be performed on a resource. For example, an application resource may
    support create, update, delete, and reset password actions.
    """

    allowedResourceActions: StringCollection = field(default_factory=StringCollection)
    condition: str | None = None
    excludedResourceActions: StringCollection = field(default_factory=StringCollection)
