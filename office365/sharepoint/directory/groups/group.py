from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from typing_extensions import Self

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.directory.helper import SPHelper
from office365.sharepoint.directory.members_info import MembersInfo
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.permissions import SiteLevel, site_access

if TYPE_CHECKING:
    from office365.sharepoint.directory.users.user import User


class Group(Entity):
    """Represents a directory group in SharePoint."""

    def get_members_info(self, row_limit: int) -> MembersInfo:
        """Gets information about the group members.

        Args:
            row_limit: Maximum number of members to return

        Returns:
            MembersInfo object containing member information
        """
        return_type = MembersInfo(self.context)

        def _get_members_info():
            from office365.sharepoint.directory.helper import SPHelper

            SPHelper.get_members_info(self.context, self.properties["Id"], row_limit, return_type)

        self.ensure_property("Id").after_execute(lambda _: _get_members_info())
        return return_type

    def get_members(self):
        """Gets the group's members.

        Returns:
            Collection of User objects representing group members
        """
        from office365.sharepoint.directory.users.user import User

        return_type = EntityCollection(self.context, User)

        def _group_loaded():
            SPHelper.get_members(self.context, self.properties["Id"], return_type)

        self.ensure_property("Id").after_execute(lambda _: _group_loaded())
        return return_type

    def get_owners(self) -> EntityCollection[User]:
        """Gets the group's owners.

        Returns:
            Collection of User objects representing group owners
        """
        from office365.sharepoint.directory.users.user import User

        return_type = EntityCollection[User](self.context, User)

        def _get_owners():
            SPHelper.get_owners(self.context, self.properties["Id"], return_type)

        self.ensure_property("Id").after_execute(lambda _: _get_owners())
        return return_type

    @property
    def entity_type_name(self):
        return "SP.Directory.Group"

    @site_access(SiteLevel.MANAGE)
    def set_user_as_owner(self, owner_id: int) -> Self:
        """SetUserAsOwner operation.

        Args:
            owner_id (int): ownerId parameter
        """
        qry = ServiceOperationQuery(self, "SetUserAsOwner", None, {"ownerId": owner_id}, None, None)
        self.context.add_query(qry)
        return self

    @odata(name="alias")
    @property
    def alias(self) -> Optional[str]:
        """Gets the alias property"""
        return self.properties.get("alias", None)

    @odata(name="allowToAddGuests")
    @property
    def allow_to_add_guests(self) -> Optional[bool]:
        """Gets the allowToAddGuests property"""
        return self.properties.get("allowToAddGuests", None)

    @odata(name="assignedLabels")
    @property
    def assigned_labels(self) -> Optional[str]:
        """Gets the assignedLabels property"""
        return self.properties.get("assignedLabels", None)

    @odata(name="calendarUrl")
    @property
    def calendar_url(self) -> Optional[str]:
        """Gets the calendarUrl property"""
        return self.properties.get("calendarUrl", None)

    @odata(name="classification")
    @property
    def classification(self) -> Optional[str]:
        """Gets the classification property"""
        return self.properties.get("classification", None)

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

    @odata(name="documentsUrl")
    @property
    def documents_url(self) -> Optional[str]:
        """Gets the documentsUrl property"""
        return self.properties.get("documentsUrl", None)

    @odata(name="editGroupUrl")
    @property
    def edit_group_url(self) -> Optional[str]:
        """Gets the editGroupUrl property"""
        return self.properties.get("editGroupUrl", None)

    @odata(name="id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the id property"""
        return self.properties.get("id", None)

    @odata(name="inboxUrl")
    @property
    def inbox_url(self) -> Optional[str]:
        """Gets the inboxUrl property"""
        return self.properties.get("inboxUrl", None)

    @odata(name="isDynamic")
    @property
    def is_dynamic(self) -> Optional[bool]:
        """Gets the isDynamic property"""
        return self.properties.get("isDynamic", None)

    @odata(name="isPublic")
    @property
    def is_public(self) -> Optional[bool]:
        """Gets the isPublic property"""
        return self.properties.get("isPublic", None)

    @odata(name="mail")
    @property
    def mail(self) -> Optional[str]:
        """Gets the mail property"""
        return self.properties.get("mail", None)

    @odata(name="notebookUrl")
    @property
    def notebook_url(self) -> Optional[str]:
        """Gets the notebookUrl property"""
        return self.properties.get("notebookUrl", None)

    @odata(name="peopleUrl")
    @property
    def people_url(self) -> Optional[str]:
        """Gets the peopleUrl property"""
        return self.properties.get("peopleUrl", None)

    @odata(name="pictureUrl")
    @property
    def picture_url(self) -> Optional[str]:
        """Gets the pictureUrl property"""
        return self.properties.get("pictureUrl", None)

    @odata(name="principalName")
    @property
    def principal_name(self) -> Optional[str]:
        """Gets the principalName property"""
        return self.properties.get("principalName", None)

    @odata(name="siteUrl")
    @property
    def site_url(self) -> Optional[str]:
        """Gets the siteUrl property"""
        return self.properties.get("siteUrl", None)

    @odata(name="members", navigation=True)
    @property
    def members(self) -> EntityCollection[User]:
        """Gets the members property"""
        from office365.sharepoint.directory.users.user import User

        return self.properties.get(
            "members", EntityCollection[User](self.context, User, ResourcePath("members", self.resource_path))
        )

    @odata(name="owners", navigation=True)
    @property
    def owners(self) -> EntityCollection[User]:
        """Gets the owners property"""
        from office365.sharepoint.directory.users.user import User

        return self.properties.get(
            "owners", EntityCollection[User](self.context, User, ResourcePath("owners", self.resource_path))
        )

    @site_access(SiteLevel.MANAGE)
    def delete(self) -> Self:
        """Delete operation."""
        qry = ServiceOperationQuery(self, "Delete", None, {}, None, None)
        self.context.add_query(qry)
        return self
