from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ExceptionDetails(ClientValue):
    message: Optional[str] = None
    stack_trace: Optional[str] = None
