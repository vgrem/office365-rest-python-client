from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.permissions.base_permissions import BasePermissions


class CustomActionElement(ClientValue):
    """A class specifies a custom action element."""

    def __init__(
        self,
        clientside_component_id: Optional[str] = None,
        client_side_component_properties: Optional[str] = None,
        command_ui_extension: Optional[str] = None,
        enabled_script: Optional[str] = None,
        host_properties: Optional[str] = None,
        image_url: Optional[str] = None,
        id_: Optional[str] = None,
        location: Optional[str] = None,
        registration_id: Optional[str] = None,
        registration_type: Optional[int] = None,
        require_site_administrator: Optional[bool] = None,
        rights: BasePermissions = BasePermissions(),
        title: Optional[str] = None,
        url_action: Optional[str] = None,
    ):
        """
        :param str clientside_component_id: The unique identifier of the client-side component associated
            with the custom action.
        :param str client_side_component_properties: This property is only used when a ClientSideComponentId is
            specified. It is optional. If non-empty, the string MUST contain a JSON object with custom
            initialization properties whose format and meaning are defined by the client-side component.
        :param str command_ui_extension: This property is only used when a ClientSideComponentId is specified.
        :param str enabled_script: The client side script to enabled or disable the custom action.
        """
        self.ClientSideComponentId = clientside_component_id
        self.ClientSideComponentProperties = client_side_component_properties
        self.CommandUIExtension = command_ui_extension
        self.EnabledScript = enabled_script
        self.HostProperties = host_properties
        self.ImageUrl = image_url
        self.Id = id_
        self.Location = location
        self.RegistrationId = registration_id
        self.RegistrationType = registration_type
        self.RequireSiteAdministrator = require_site_administrator
        self.Rights = rights
        self.Title = title
        self.UrlAction = url_action
