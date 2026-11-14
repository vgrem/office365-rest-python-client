from __future__ import annotations

from office365.communications.callrecords.service_role import ServiceRole
from office365.communications.callrecords.user_agent import UserAgent


class ServiceUserAgent(UserAgent):
    role: ServiceRole = ServiceRole.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.ServiceUserAgent"
