from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class EnsureTeamForGroupExResponse(ClientValue):
    teamsId: Optional[str] = None
    teamsUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.EnsureTeamForGroupExResponse"
