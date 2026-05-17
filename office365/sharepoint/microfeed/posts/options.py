from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.microfeed.datalinkcollection import (
    MicrofeedDataLinkCollection,
)
from office365.sharepoint.microfeed.link import MicrofeedLink


class MicrofeedPostOptions(ClientValue):
    def __init__(
        self,
        content: Optional[str] = None,
        content_formatting_option: Optional[int] = None,
        data_links: MicrofeedDataLinkCollection = MicrofeedDataLinkCollection(),
        definition_name: Optional[str] = None,
        media_link: MicrofeedLink = MicrofeedLink(),
        people_list: StringCollection = StringCollection(),
        post_source: Optional[str] = None,
        post_source_uri: Optional[str] = None,
        ref_thread__reference_id: Optional[str] = None,
        ref_thread__ref_reply: Optional[str] = None,
        ref_thread__ref_root: Optional[str] = None,
        target_actor: Optional[str] = None,
        update_status_text: Optional[bool] = None,
    ):
        self.Content = content
        self.ContentFormattingOption = content_formatting_option
        self.DataLinks = data_links
        self.DefinitionName = definition_name
        self.MediaLink = media_link
        self.PeopleList = people_list
        self.PostSource = post_source
        self.PostSourceUri = post_source_uri
        self.RefThread_ReferenceID = ref_thread__reference_id
        self.RefThread_RefReply = ref_thread__ref_reply
        self.RefThread_RefRoot = ref_thread__ref_root
        self.TargetActor = target_actor
        self.UpdateStatusText = update_status_text

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedPostOptions"
