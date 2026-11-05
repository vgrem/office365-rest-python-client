from __future__ import annotations

from office365.directory.applications.weakalgorithms import WeakAlgorithms
from office365.runtime.client_value import ClientValue


class RequestSignatureVerification(ClientValue):
    allowedWeakAlgorithms: WeakAlgorithms | None = None
    isSignedRequestRequired: bool | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.RequestSignatureVerification"
