from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class TaxonomyReplicationParameters(Entity):
    @odata(name="IsReplicateAllContentTypes")
    @property
    def is_replicate_all_content_types(self) -> Optional[bool]:
        """Gets the IsReplicateAllContentTypes property"""
        return self.properties.get("IsReplicateAllContentTypes", None)

    @odata(name="IsReplicateAllGroups")
    @property
    def is_replicate_all_groups(self) -> Optional[bool]:
        """Gets the IsReplicateAllGroups property"""
        return self.properties.get("IsReplicateAllGroups", None)

    @odata(name="ReplicatedContentTypes")
    @property
    def replicated_content_types(self) -> Optional[StringCollection]:
        """Gets the ReplicatedContentTypes property"""
        return self.properties.get("ReplicatedContentTypes", None)

    @odata(name="ReplicatedGroups")
    @property
    def replicated_groups(self) -> Optional[StringCollection]:
        """Gets the ReplicatedGroups property"""
        return self.properties.get("ReplicatedGroups", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.TaxonomyReplicationParameters"
