from office365.runtime.client_value import ClientValue


class CampaignPublicationSaveMailDraftParam(ClientValue):

    def __init__(self, is_opx_content_modified: bool = None):
        self.IsOpxContentModified = is_opx_content_modified
