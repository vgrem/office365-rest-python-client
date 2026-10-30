from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions.base_permissions import BasePermissions

if TYPE_CHECKING:
    from office365.sharepoint.translation.user_resource import UserResource


class UserCustomAction(Entity):
    """Represents a custom action associated with a SharePoint list, Web site, or subsite."""

    @odata(name="ClientSideComponentId", beta=True)
    @property
    def client_side_component_id(self) -> Optional[str]:
        """"""
        return self.properties.get("ClientSideComponentId", None)

    @odata(name="ScriptBlock")
    @property
    def script_block(self) -> Optional[str]:
        """Gets the value that specifies the ECMAScript to be executed when the custom action is performed."""
        return self.properties.get("ScriptBlock", None)

    @script_block.setter
    def script_block(self, value: str) -> None:
        """
        Sets the value that specifies the ECMAScript to be executed when the custom action is performed.
        """
        self.set_property("ScriptBlock", value)

    @odata(name="ScriptSrc")
    @property
    def script_src(self) -> Optional[str]:
        """Gets a value that specifies the URI of a file which contains the ECMAScript to execute on the page"""
        return self.properties.get("ScriptSrc", None)

    @script_src.setter
    def script_src(self, value: str) -> None:
        """
        Sets a value that specifies the URI of a file which contains the ECMAScript to execute on the page
        """
        self.set_property("ScriptSrc", value)

    @odata(name="Url")
    @property
    def url(self) -> Optional[str]:
        """Gets or sets the URL, URI, or ECMAScript (JScript, JavaScript) function associated with the action."""
        return self.properties.get("Url", None)

    @odata(name="ClientSideComponentProperties", beta=True)
    @property
    def client_side_component_properties(self) -> Optional[str]:
        """Gets the ClientSideComponentProperties property"""
        return self.properties.get("ClientSideComponentProperties", None)

    @odata(name="CommandUIExtension")
    @property
    def command_ui_extension(self) -> Optional[str]:
        """Gets the CommandUIExtension property"""
        return self.properties.get("CommandUIExtension", None)

    @odata(name="Description")
    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @odata(name="Group")
    @property
    def group(self) -> Optional[str]:
        """Gets the Group property"""
        return self.properties.get("Group", None)

    @odata(name="HostProperties", beta=True)
    @property
    def host_properties(self) -> Optional[str]:
        """Gets the HostProperties property"""
        return self.properties.get("HostProperties", None)

    @odata(name="Id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    @odata(name="ImageUrl")
    @property
    def image_url(self) -> Optional[str]:
        """Gets the ImageUrl property"""
        return self.properties.get("ImageUrl", None)

    @odata(name="Location")
    @property
    def location(self) -> Optional[str]:
        """Gets the Location property"""
        return self.properties.get("Location", None)

    @odata(name="Name")
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @odata(name="RegistrationId")
    @property
    def registration_id(self) -> Optional[str]:
        """Gets the RegistrationId property"""
        return self.properties.get("RegistrationId", None)

    @odata(name="RegistrationType")
    @property
    def registration_type(self) -> Optional[int]:
        """Gets the RegistrationType property"""
        return self.properties.get("RegistrationType", None)

    @odata(name="Rights")
    @property
    def rights(self) -> BasePermissions:
        """Gets the Rights property"""
        return self.properties.get("Rights", BasePermissions())

    @odata(name="Scope")
    @property
    def scope(self) -> Optional[int]:
        """Gets the Scope property"""
        return self.properties.get("Scope", None)

    @odata(name="Sequence")
    @property
    def sequence(self) -> Optional[int]:
        """Gets the Sequence property"""
        return self.properties.get("Sequence", None)

    @odata(name="Title")
    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @odata(name="VersionOfUserCustomAction")
    @property
    def version_of_user_custom_action(self) -> Optional[str]:
        """Gets the VersionOfUserCustomAction property"""
        return self.properties.get("VersionOfUserCustomAction", None)

    @odata(name="DescriptionResource", navigation=True)
    @property
    def description_resource(self) -> UserResource:
        """Gets the DescriptionResource property"""
        from office365.sharepoint.translation.user_resource import UserResource

        return self.properties.get(
            "DescriptionResource", UserResource(self.context, ResourcePath("DescriptionResource", self.resource_path))
        )

    @odata(name="TitleResource", navigation=True)
    @property
    def title_resource(self) -> UserResource:
        """Gets the TitleResource property"""
        from office365.sharepoint.translation.user_resource import UserResource

        return self.properties.get(
            "TitleResource", UserResource(self.context, ResourcePath("TitleResource", self.resource_path))
        )
