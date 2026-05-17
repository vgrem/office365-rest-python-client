from typing import Optional

from office365.runtime.client_value import ClientValue


class CampaignPublicationSaveMailDraftParam(ClientValue):
    def __init__(self, is_opx_content_modified: Optional[bool] = None):
        self.IsOpxContentModified = is_opx_content_modified

    @property
    def entity_type_name(self):
        return "SP.Publishing.CampaignPublicationSaveMailDraftParam"
