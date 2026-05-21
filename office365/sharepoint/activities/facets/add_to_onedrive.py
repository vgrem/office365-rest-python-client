from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AddToOneDriveFacet(ClientValue):
    """
    :param str added_datetime:
    :param str mount_point_name:
    :param str removed_datetime:
    """
    addedDateTime: str | None = None
    mountPointName: str | None = None
    removedDateTime: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.AddToOneDriveFacet"
