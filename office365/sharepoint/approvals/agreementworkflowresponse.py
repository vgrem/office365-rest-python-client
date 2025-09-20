from office365.runtime.client_value import ClientValue


class AgreementWorkFlowResponse(ClientValue):

    def __init__(self, next_work_flow: str = None):
        self.next_work_flow = next_work_flow
