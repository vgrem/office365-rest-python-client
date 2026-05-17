from typing import Optional

from office365.runtime.client_value import ClientValue


class CampaignPublicationLoadMailDraftParam(ClientValue):
    def __init__(self, is_preview: Optional[bool] = None):
        self.IsPreview = is_preview

    @property
    def entity_type_name(self):
        return "SP.Publishing.CampaignPublicationLoadMailDraftParam"
