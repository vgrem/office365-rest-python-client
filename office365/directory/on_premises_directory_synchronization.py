from __future__ import annotations

from office365.directory.synchronization.on_premises_directory_synchronization_configuration import (  # noqa: E501
    OnPremisesDirectorySynchronizationConfiguration,
)
from office365.directory.synchronization.on_premises_directory_synchronization_feature import (  # noqa: E501
    OnPremisesDirectorySynchronizationFeature,
)
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class OnPremisesDirectorySynchronization(Entity):
    @odata(name="configuration")
    @property
    def configuration(self) -> OnPremisesDirectorySynchronizationConfiguration:
        """Gets the configuration property"""
        return self.properties.get("configuration", OnPremisesDirectorySynchronizationConfiguration())

    @odata(name="features")
    @property
    def features(self) -> OnPremisesDirectorySynchronizationFeature:
        """Gets the features property"""
        return self.properties.get("features", OnPremisesDirectorySynchronizationFeature())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnPremisesDirectorySynchronization"
