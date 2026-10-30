from __future__ import annotations

from typing import Optional

from office365.directory.audit.outliercontainertype import OutlierContainerType
from office365.directory.audit.outliermembertype import OutlierMemberType
from office365.directory.audit.signins.governance_insight import GovernanceInsight
from office365.directory.objects.object import DirectoryObject
from office365.directory.users.user import User
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class MembershipOutlierInsight(GovernanceInsight):
    @odata(name="containerId")
    @property
    def container_id(self) -> Optional[str]:
        """Gets the containerId property"""
        return self.properties.get("containerId", None)

    @odata(name="memberId")
    @property
    def member_id(self) -> Optional[str]:
        """Gets the memberId property"""
        return self.properties.get("memberId", None)

    @odata(name="outlierContainerType")
    @property
    def outlier_container_type(self) -> OutlierContainerType:
        """Gets the outlierContainerType property"""
        return self.properties.get("outlierContainerType", OutlierContainerType.group)

    @odata(name="outlierMemberType")
    @property
    def outlier_member_type(self) -> OutlierMemberType:
        """Gets the outlierMemberType property"""
        return self.properties.get("outlierMemberType", OutlierMemberType.user)

    @odata(name="container", navigation=True)
    @property
    def container(self) -> DirectoryObject:
        """Gets the container property"""
        return self.properties.get(
            "container", DirectoryObject(self.context, ResourcePath("container", self.resource_path))
        )

    @odata(name="lastModifiedBy", navigation=True)
    @property
    def last_modified_by(self) -> User:
        """Gets the lastModifiedBy property"""
        return self.properties.get(
            "lastModifiedBy", User(self.context, ResourcePath("lastModifiedBy", self.resource_path))
        )

    @odata(name="member", navigation=True)
    @property
    def member(self) -> DirectoryObject:
        """Gets the member property"""
        return self.properties.get("member", DirectoryObject(self.context, ResourcePath("member", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MembershipOutlierInsight"
