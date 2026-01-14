from office365.runtime.client_value import ClientValue


class CampaignPublicationMailDraftData(ClientValue):
    def __init__(self, draft_id: str = None, group_upn: str = None):
        self.DraftId = draft_id
        self.GroupUpn = group_upn

    " "

    @property
    def entity_type_name(self):
        return "SP.Publishing.CampaignPublicationMailDraftData"
