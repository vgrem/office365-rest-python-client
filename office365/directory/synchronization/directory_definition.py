from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.synchronization.directorydefinitiondiscoverabilities import DirectoryDefinitionDiscoverabilities
from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb
from office365.security.object_definition import ObjectDefinition

if TYPE_CHECKING:
    from office365.directory.synchronization.directory_definition import DirectoryDefinition


class DirectoryDefinition(Entity):
    """
    Provides the synchronization engine information about a directory and its objects. This resource tells the
    synchronization engine, for example, that the directory has objects named user and group, which attributes are
    supported for those objects, and the types for those attributes. In order for the object and attribute to
    participate in synchronization rules and object mappings, they must be defined as part of the directory definition.

    Directory definitions are updated as part of the synchronization schema.
    """

    @odata(name="discoverabilities")
    @property
    def discoverabilities(self) -> DirectoryDefinitionDiscoverabilities:
        """Gets the discoverabilities property"""
        return self.properties.get("discoverabilities", DirectoryDefinitionDiscoverabilities.Unknown)

    @odata(name="discoveryDateTime")
    @property
    def discovery_date_time(self) -> datetime:
        """Gets the discoveryDateTime property"""
        return self.properties.get("discoveryDateTime", datetime.min)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="objects")
    @property
    def objects(self) -> ClientValueCollection[ObjectDefinition]:
        """Gets the objects property"""
        return self.properties.get("objects", ClientValueCollection[ObjectDefinition](ObjectDefinition))

    @odata(name="readOnly")
    @property
    def read_only(self) -> Optional[bool]:
        """Gets the readOnly property"""
        return self.properties.get("readOnly", None)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DirectoryDefinition"

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["Directory.ReadWrite.All"],
        application=["Application.ReadWrite.OwnedBy", "Directory.ReadWrite.All"],
    )
    def discover(self) -> DirectoryDefinition:
        """discover operation."""
        from office365.directory.synchronization.directory_definition import DirectoryDefinition

        return_type = DirectoryDefinition(self.context)
        qry = ServiceOperationQuery(self, "discover", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
