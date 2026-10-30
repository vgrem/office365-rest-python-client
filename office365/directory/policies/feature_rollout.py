from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.directory.objects.collection import DirectoryObjectCollection
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.policies.stagedfeaturename import StagedFeatureName


class FeatureRolloutPolicy(Entity):
    """
    Represents a feature rollout policy associated with a directory object. Creating a feature rollout policy
    helps tenant administrators to pilot features of Microsoft Entra ID with a specific group before enabling
    features for entire organization. This minimizes the impact and helps administrators to test and rollout
    authentication related features gradually.

    The following are limitations of feature rollout:

     - Each feature supports a maximum of 10 groups.
     - The appliesTo field only supports groups.
     - Dynamic groups and nested groups are not supported.
    """

    @odata(name="appliesTo", navigation=True)
    @property
    def applies_to(self) -> DirectoryObjectCollection:
        """
        Specifies a list of directoryObject resources that feature is enabled for.
        """
        return self.properties.get(
            "appliesTo",
            DirectoryObjectCollection(
                self.context,
                ResourcePath("appliesTo", self.resource_path),
            ),
        )

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="feature")
    @property
    def feature(self) -> StagedFeatureName:
        """Gets the feature property"""
        from office365.directory.policies.stagedfeaturename import StagedFeatureName

        return self.properties.get("feature", StagedFeatureName.passthroughAuthentication)

    @odata(name="isAppliedToOrganization")
    @property
    def is_applied_to_organization(self) -> Optional[bool]:
        """Gets the isAppliedToOrganization property"""
        return self.properties.get("isAppliedToOrganization", None)

    @odata(name="isEnabled")
    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the isEnabled property"""
        return self.properties.get("isEnabled", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.FeatureRolloutPolicy"
