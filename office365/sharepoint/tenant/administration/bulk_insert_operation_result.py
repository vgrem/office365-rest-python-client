from __future__ import annotations

from dataclasses import field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.authoritative_resource_properties import AuthoritativeResourceProperties


class BulkInsertOperationResult(ClientValue):
    ErrorMessage: str | None = None
    IsSuccess: bool | None = None
    SiteId: UUID | None = None
    AuthoritativeResourceProperties: AuthoritativeResourceProperties = field(
        default_factory=AuthoritativeResourceProperties
    )

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.BulkInsertOperationResult"
