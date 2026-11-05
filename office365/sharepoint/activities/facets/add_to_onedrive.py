from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AddToOneDriveFacet(ClientValue):
    """Args:
    added_datetime (str):
    mount_point_name (str):
    removed_datetime (str):
    """

    addedDateTime: str | None = None
    mountPointName: str | None = None
    removedDateTime: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.AddToOneDriveFacet"
