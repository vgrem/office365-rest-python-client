from office365.directory.objects.collection import DirectoryObjectCollection
from office365.directory.policies.base import PolicyBase
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class StsPolicy(PolicyBase):
    """Represents an abstract base type for policy types that control Microsoft identity platform behavior."""

    @odata(name="appliesTo")
    @property
    def applies_to(self) -> DirectoryObjectCollection:
        """"""
        return self.properties.get(
            "appliesTo",
            DirectoryObjectCollection(self.context, ResourcePath("appliesTo", self.resource_path)),
        )
