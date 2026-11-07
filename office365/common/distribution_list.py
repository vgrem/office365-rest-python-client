from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.common.distribution_list import DistributionList
    from office365.common.distribution_list_member import DistributionListMember
    from office365.common.member import Member
    from office365.directory.extensions.extended_property import SingleValueLegacyExtendedProperty


class DistributionList(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="notes")
    @property
    def notes(self) -> Optional[str]:
        """Gets the notes property"""
        return self.properties.get("notes", None)

    @odata(name="personId")
    @property
    def person_id(self) -> Optional[str]:
        """Gets the personId property"""
        return self.properties.get("personId", None)

    @odata(name="members", navigation=True)
    @property
    def members(self) -> EntityCollection[DistributionListMember]:
        """Gets the members property"""
        from office365.common.distribution_list_member import DistributionListMember

        return self.properties.get(
            "members",
            EntityCollection[DistributionListMember](
                self.context, DistributionListMember, ResourcePath("members", self.resource_path)
            ),
        )

    @odata(name="singleValueExtendedProperties", navigation=True)
    @property
    def single_value_extended_properties(self) -> EntityCollection[SingleValueLegacyExtendedProperty]:
        """Gets the singleValueExtendedProperties property"""
        from office365.directory.extensions.extended_property import SingleValueLegacyExtendedProperty

        return self.properties.get(
            "singleValueExtendedProperties",
            EntityCollection[SingleValueLegacyExtendedProperty](
                self.context,
                SingleValueLegacyExtendedProperty,
                ResourcePath("singleValueExtendedProperties", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DistributionList"

    def add_members(self, members: ClientValueCollection[Member]) -> DistributionList:
        """addMembers operation.

        Args:
            members (ClientValueCollection[Member]):
                Members parameter
        """
        from office365.common.distribution_list import DistributionList

        return_type = DistributionList(self.context)
        qry = ServiceOperationQuery(self, "addMembers", None, {"Members": members}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def delete_members(self, members: ClientValueCollection[Member]) -> DistributionList:
        """deleteMembers operation.

        Args:
            members (ClientValueCollection[Member]):
                Members parameter
        """
        from office365.common.distribution_list import DistributionList

        return_type = DistributionList(self.context)
        qry = ServiceOperationQuery(self, "deleteMembers", None, {"Members": members}, None, return_type)
        self.context.add_query(qry)
        return return_type
