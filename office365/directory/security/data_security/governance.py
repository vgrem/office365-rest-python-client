from office365.directory.security.data_security.sensitivity_label import SensitivityLabel
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class TenantDataSecurityAndGovernance(Entity):
    """Tenant-level container for data security and governance settings."""

    @odata(name="sensitivityLabels")
    @property
    def sensitivity_labels(self) -> EntityCollection[SensitivityLabel]:
        return self.properties.get(
            "sensitivityLabels",
            EntityCollection(self.context, SensitivityLabel, ResourcePath("sensitivityLabels", self.resource_path)),
        )
