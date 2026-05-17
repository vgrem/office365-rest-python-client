from typing import Optional

from office365.runtime.client_value import ClientValue


class ExceptionDetails(ClientValue):
    def __init__(self, message: Optional[str] = None, stack_trace: Optional[str] = None):
        self.message = message
        self.stack_trace = stack_trace
