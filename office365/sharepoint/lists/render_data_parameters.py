from office365.runtime.client_value import ClientValue


class RenderListDataParameters(ClientValue):
    """Specifies the parameters to be used to render list data as a JSON string"""

    def __init__(
        self,
        add_all_fields: bool = None,
        add_all_view_fields: bool = None,
        add_regional_settings: bool = None,
        add_required_fields=None,
        allow_multiple_value_filter_for_taxonomy_fields=None,
        audience_target=None,
        dates_in_utc=None,
        expand_groups=None,
        expand_user_field=None,
        filter_out_channel_folders_in_default_doc_lib=None,
        render_options=None,
        require_folder_coloring_fields=None,
        show_stub_file=None,
        view_xml: str = None,
        first_group_only: bool = None,
        folder_server_relative_url: str = None,
        image_fields_to_try_rewrite_to_cdn_urls: str = None,
        merge_default_view: bool = None,
        modern_list_boot: bool = None,
        original_date: bool = None,
        override_view_xml: str = None,
        paging: str = None,
        render_url_field_in_json: bool = None,
        replace_group: bool = None,
    ):
        """
        :param bool add_all_fields:
        :param bool add_all_view_fields:
        :param bool add_regional_settings:
        :param bool add_required_fields: This parameter indicates if we return required fields.
        :param bool allow_multiple_value_filter_for_taxonomy_fields: This parameter indicates whether multi value
            filtering is allowed for taxonomy fields.
        :param bool audience_target:
        :param bool dates_in_utc: Specifies if the DateTime field is returned in UTC or local time.
        :param bool expand_groups: Specifies whether to expand the grouping or not.
        :param bool expand_user_field:
        :param bool filter_out_channel_folders_in_default_doc_lib:
        :param int render_options: Specifies the type of output to return.
        :param bool require_folder_coloring_fields:
        :param bool show_stub_file:
        :param str view_xml: Specifies the CAML view XML.
        """
        self.AddAllFields = add_all_fields
        self.AddAllViewFields = add_all_view_fields
        self.AddRegionalSettings = add_regional_settings
        self.AddRequiredFields = add_required_fields
        self.AllowMultipleValueFilterForTaxonomyFields = (
            allow_multiple_value_filter_for_taxonomy_fields
        )
        self.AudienceTarget = audience_target
        self.DatesInUtc = dates_in_utc
        self.ExpandGroups = expand_groups
        self.ExpandUserField = expand_user_field
        self.FilterOutChannelFoldersInDefaultDocLib = (
            filter_out_channel_folders_in_default_doc_lib
        )
        self.RenderOptions = render_options
        self.RequireFolderColoringFields = require_folder_coloring_fields
        self.ShowStubFile = show_stub_file
        self.ViewXml = view_xml
        self.FirstGroupOnly = first_group_only
        self.FolderServerRelativeUrl = folder_server_relative_url
        self.ImageFieldsToTryRewriteToCdnUrls = image_fields_to_try_rewrite_to_cdn_urls
        self.MergeDefaultView = merge_default_view
        self.ModernListBoot = modern_list_boot
        self.OriginalDate = original_date
        self.OverrideViewXml = override_view_xml
        self.Paging = paging
        self.RenderURLFieldInJSON = render_url_field_in_json
        self.ReplaceGroup = replace_group

    @property
    def entity_type_name(self):
        return "SP.RenderListDataParameters"
