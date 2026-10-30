from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class DelegatedAdminServiceProviderConstraints(Entity):
    @odata(name="allowedRoleTemplateIds")
    @property
    def allowed_role_template_ids(self) -> StringCollection:
        """Gets the allowedRoleTemplateIds property"""
        return self.properties.get("allowedRoleTemplateIds", StringCollection())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DelegatedAdminServiceProviderConstraints"
