from office365.runtime.client_value import ClientValue


class CustomActionElement(ClientValue):
    """A class specifies a custom action element."""

    def __init__(
        self,
        clientside_component_id=None,
        client_side_component_properties=None,
        command_ui_extension=None,
        enabled_script=None,
        host_properties=None,
        image_url=None,
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
