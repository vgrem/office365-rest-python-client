from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class TaxonomyReplicationParameters(Entity):

    @property
    def is_replicate_all_content_types(self) -> Optional[bool]:
        """Gets the IsReplicateAllContentTypes property"""
        return self.properties.get("IsReplicateAllContentTypes", None)

    @property
    def is_replicate_all_groups(self) -> Optional[bool]:
        """Gets the IsReplicateAllGroups property"""
        return self.properties.get("IsReplicateAllGroups", None)

    @property
    def replicated_content_types(self) -> StringCollection:
        """Gets the ReplicatedContentTypes property"""
        return self.properties.get("ReplicatedContentTypes", None)

    @property
    def replicated_groups(self) -> StringCollection:
        """Gets the ReplicatedGroups property"""
        return self.properties.get("ReplicatedGroups", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MultiGeo.Service.TaxonomyReplicationParameters"
