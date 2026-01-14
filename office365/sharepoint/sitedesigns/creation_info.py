import uuid

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


class SiteDesignCreationInfo(ClientValue):
    def __init__(
        self,
        _id=None,
        title=None,
        description=None,
        web_template=None,
        site_script_ids=None,
        design_package_id=None,
        design_type=None,
        internal_name=None,
        is_default=None,
        is_out_of_box_template=None,
        is_tenant_admin_only=None,
        list_color=None,
        list_icon=None,
        preview_image_alt_text=None,
        preview_image_url=None,
        requires_class_connected=None,
        requires_group_connected=None,
        requires_syntex_license=None,
        requires_teams_connected=None,
        requires_yammer_connected=None,
        supported_web_templates=None,
    ):
        """:param str or None _id: The ID of the site design to apply.
        :param str or None title: The display name of the site design.
        :param str or None description: The display description of site design.
        :param str or None web_template: Identifies which base template to add the design to. Use the value 64 for the
            Team site template, and the value 68 for the Communication site template.
        :param list[UUID] or None site_script_ids: A list of one or more site scripts. Each is identified by an ID.
            The scripts will run in the order listed.
        :param str or None design_package_id:
        """
        self.Id = _id
        self.Title = title
        self.Description = description
        self.WebTemplate = web_template
        self.SiteScriptIds = ClientValueCollection(uuid.UUID, site_script_ids)
        self.DesignPackageId = design_package_id
        self.DesignType = design_type
        self.InternalName = internal_name
        self.IsDefault = is_default
        self.IsOutOfBoxTemplate = is_out_of_box_template
        self.IsTenantAdminOnly = is_tenant_admin_only
        self.ListColor = list_color
        self.ListIcon = list_icon
        self.PreviewImageAltText = preview_image_alt_text
        self.PreviewImageUrl = preview_image_url
        self.RequiresClassConnected = requires_class_connected
        self.RequiresGroupConnected = requires_group_connected
        self.RequiresSyntexLicense = requires_syntex_license
        self.RequiresTeamsConnected = requires_teams_connected
        self.RequiresYammerConnected = requires_yammer_connected
        self.SupportedWebTemplates = StringCollection(supported_web_templates)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignCreationInfo"
