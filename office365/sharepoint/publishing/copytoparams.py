from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class CopyToParams(ClientValue):
    def __init__(
        self,
        as_news: Optional[bool] = None,
        as_private_authoring_page: Optional[bool] = None,
        as_template: Optional[bool] = None,
        canvas_content_only: Optional[bool] = None,
        component_json_string: Optional[str] = None,
        create_copy_for_edit: Optional[bool] = None,
        create_copy_with_title_suffix: Optional[bool] = None,
        create_if_missing: Optional[bool] = None,
        delete_source_page: Optional[bool] = None,
        dependency_property_types_to_deep_copy: ClientValueCollection[int] = ClientValueCollection(int),
        destination_page_unique_id: Optional[str] = None,
        destination_type: Optional[int] = None,
        destination_web_url: Optional[str] = None,
        scenario_id: Optional[int] = None,
        scenario_payload: Optional[str] = None,
        should_add_fallback_link_for_video_for_amplify: Optional[bool] = None,
        site_page_flags: Optional[str] = None,
    ):
        self.AsNews = as_news
        self.AsPrivateAuthoringPage = as_private_authoring_page
        self.AsTemplate = as_template
        self.CanvasContentOnly = canvas_content_only
        self.ComponentJSONString = component_json_string
        self.CreateCopyForEdit = create_copy_for_edit
        self.CreateCopyWithTitleSuffix = create_copy_with_title_suffix
        self.CreateIfMissing = create_if_missing
        self.DeleteSourcePage = delete_source_page
        self.DependencyPropertyTypesToDeepCopy = dependency_property_types_to_deep_copy
        self.DestinationPageUniqueId = destination_page_unique_id
        self.DestinationType = destination_type
        self.DestinationWebUrl = destination_web_url
        self.ScenarioID = scenario_id
        self.ScenarioPayload = scenario_payload
        self.ShouldAddFallbackLinkForVideoForAmplify = should_add_fallback_link_for_video_for_amplify
        self.SitePageFlags = site_page_flags

    @property
    def entity_type_name(self):
        return "SP.Publishing.CopyToParams"
