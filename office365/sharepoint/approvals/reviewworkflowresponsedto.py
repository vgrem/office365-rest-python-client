from office365.runtime.client_value import ClientValue


class ReviewWorkFlowResponseDTO(ClientValue):
    def __init__(self, action: str = None, comments: str = None, status: str = None):
        self.action = action
        self.comments = comments
        self.status = status
