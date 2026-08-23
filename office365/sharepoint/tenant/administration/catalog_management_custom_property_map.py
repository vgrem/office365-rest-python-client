from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.tenant.administration.site_property_scope_config import SitePropertyScopeConfig


class CatalogManagementCustomPropertyMap(ClientValue):
    lastUpdatedTimeUtc: datetime | None = field(default_factory=lambda: datetime.min)
    maxSiteCount: int | None = None
    pendingScanSlots: StringCollection = field(default_factory=StringCollection)
    sitePropertyDisplayNames: dict | None = field(default_factory=dict)
    sitePropertyMapping: dict | None = field(default_factory=dict)
    lastAppliedSitePropertyMapping: dict | None = field(default_factory=dict)
    sitePropertyScopeConfig: SitePropertyScopeConfig = field(default_factory=SitePropertyScopeConfig)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.CatalogManagementCustomPropertyMap"
