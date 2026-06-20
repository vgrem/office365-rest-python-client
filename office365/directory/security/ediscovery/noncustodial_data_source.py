from __future__ import annotations

from office365.directory.security.search.data_source import DataSource
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class EdiscoveryNoncustodialDataSource(Entity):
    @property
    def data_source(self) -> DataSource:
        """Gets the dataSource property"""
        return self.properties.get(
            "dataSource", DataSource(self.context, ResourcePath("dataSource", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoveryNoncustodialDataSource"
