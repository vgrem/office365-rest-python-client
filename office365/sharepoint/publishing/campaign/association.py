from office365.runtime.client_value import ClientValue


class CampaignAssociation(ClientValue):

    def __init__(self, campaign_id: int = None, publication_id: int = None):
        self.CampaignId = campaign_id
        self.PublicationId = publication_id
