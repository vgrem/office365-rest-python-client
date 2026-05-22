from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.mail.location_constraint_item import LocationConstraintItem
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class LocationConstraint(ClientValue):
    """The conditions stated by a client for the location of a meeting."""

    isRequired: bool | None = None
    locations: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(LocationConstraintItem))
    suggestLocation: bool | None = None
