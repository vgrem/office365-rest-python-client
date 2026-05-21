from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AuditResource(ClientValue):
    """A class containing the properties for Audit Resource.

    :param str audit_resource_type: Audit resource's type.
    """

    auditResourceType: str | None = None
