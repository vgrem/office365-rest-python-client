from office365.directory.objects.collection import DirectoryObjectCollection
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


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

    @odata(name="appliesTo")
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
