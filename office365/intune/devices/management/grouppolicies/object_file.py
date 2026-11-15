from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class GroupPolicyObjectFile(Entity):
    @odata(name="content")
    @property
    def content(self) -> Optional[str]:
        """Gets the content property"""
        return self.properties.get("content", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="groupPolicyObjectId")
    @property
    def group_policy_object_id(self) -> Optional[UUID]:
        """Gets the groupPolicyObjectId property"""
        return self.properties.get("groupPolicyObjectId", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="ouDistinguishedName")
    @property
    def ou_distinguished_name(self) -> Optional[str]:
        """Gets the ouDistinguishedName property"""
        return self.properties.get("ouDistinguishedName", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyObjectFile"
