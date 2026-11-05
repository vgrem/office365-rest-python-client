from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class TrackedItemUpdatesRequest(ClientValue):
    TimeStamp: datetime | None = None
    TrackedItemsAsJson: str | None = None
    UserEmail: str | None = None
    UserLogin: str | None = None
    UserPuid: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.TrackedItemUpdatesRequest"
