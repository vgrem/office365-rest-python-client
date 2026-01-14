from office365.directory.applications.weakalgorithms import WeakAlgorithms
from office365.runtime.client_value import ClientValue


class RequestSignatureVerification(ClientValue):
    def __init__(self, allowed_weak_algorithms: WeakAlgorithms = None, is_signed_request_required: bool = None):
        self.allowedWeakAlgorithms = allowed_weak_algorithms
        self.isSignedRequestRequired = is_signed_request_required

    @property
    def entity_type_name(self):
        return "microsoft.graph.RequestSignatureVerification"
