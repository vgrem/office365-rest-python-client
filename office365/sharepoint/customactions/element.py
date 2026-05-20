from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.permissions.base_permissions import BasePermissions


@dataclass
class CustomActionElement(ClientValue):
    """A class specifies a custom action element.

    :param str clientside_component_id: The unique identifier of the client-side component associated
        with the custom action.
    :param str client_side_component_properties: This property is only used when a ClientSideComponentId is
        specified. It is optional. If non-empty, the string MUST contain a JSON object with custom
        initialization properties whose format and meaning are defined by the client-side component.
    :param str command_ui_extension: This property is only used when a ClientSideComponentId is specified.
    :param str enabled_script: The client side script to enabled or disable the custom action.
    """

    ClientSideComponentId: Optional[str] = None
    ClientSideComponentProperties: Optional[str] = None
    CommandUIExtension: Optional[str] = None
    EnabledScript: Optional[str] = None
    HostProperties: Optional[str] = None
    ImageUrl: Optional[str] = None
    Id: Optional[str] = None
    Location: Optional[str] = None
    RegistrationId: Optional[str] = None
    RegistrationType: Optional[int] = None
    RequireSiteAdministrator: Optional[bool] = None
    Rights: BasePermissions = field(default_factory=BasePermissions)
    Title: Optional[str] = None
    UrlAction: Optional[str] = None
