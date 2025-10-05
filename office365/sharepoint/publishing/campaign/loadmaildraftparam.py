from office365.runtime.client_value import ClientValue


class CampaignPublicationLoadMailDraftParam(ClientValue):

    def __init__(self, is_preview: bool = None):
        self.IsPreview = is_preview
