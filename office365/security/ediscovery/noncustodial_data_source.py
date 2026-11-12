from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Self

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb
from office365.security.search.data_source import DataSource

if TYPE_CHECKING:
    from office365.security.ediscovery.ediscovery_index_operation import (
        EdiscoveryIndexOperation,
    )


class EdiscoveryNoncustodialDataSource(Entity):
    @odata(name="dataSource", navigation=True)
    @property
    def data_source(self) -> DataSource:
        """Gets the dataSource property"""
        return self.properties.get(
            "dataSource", DataSource(self.context, ResourcePath("dataSource", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoveryNoncustodialDataSource"

    @odata(name="lastIndexOperation", navigation=True)
    @property
    def last_index_operation(self) -> EdiscoveryIndexOperation:
        """Gets the lastIndexOperation property"""
        from office365.security.ediscovery.ediscovery_index_operation import (
            EdiscoveryIndexOperation,
        )

        return self.properties.get(
            "lastIndexOperation",
            EdiscoveryIndexOperation(self.context, ResourcePath("lastIndexOperation", self.resource_path)),
        )

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["eDiscovery.Read.All", "eDiscovery.ReadWrite.All"],
        application=["eDiscovery.Read.All", "eDiscovery.ReadWrite.All"],
    )
    def apply_hold(self) -> Self:
        """applyHold operation."""
        qry = ServiceOperationQuery(self, "applyHold", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["eDiscovery.Read.All", "eDiscovery.ReadWrite.All"],
        application=["eDiscovery.Read.All", "eDiscovery.ReadWrite.All"],
    )
    def release(self) -> Self:
        """release operation."""
        qry = ServiceOperationQuery(self, "release", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["eDiscovery.Read.All", "eDiscovery.ReadWrite.All"],
        application=["eDiscovery.Read.All", "eDiscovery.ReadWrite.All"],
    )
    def remove_hold(self) -> Self:
        """removeHold operation."""
        qry = ServiceOperationQuery(self, "removeHold", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["eDiscovery.Read.All", "eDiscovery.ReadWrite.All"],
        application=["eDiscovery.Read.All", "eDiscovery.ReadWrite.All"],
    )
    def update_index(self) -> Self:
        """updateIndex operation."""
        qry = ServiceOperationQuery(self, "updateIndex", None, {}, None, None)
        self.context.add_query(qry)
        return self
