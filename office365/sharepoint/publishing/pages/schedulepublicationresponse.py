from office365.runtime.client_value import ClientValue


class SchedulePublicationResponse(ClientValue):

    def __init__(self, publication_status: int = None):
        self.PublicationStatus = publication_status
