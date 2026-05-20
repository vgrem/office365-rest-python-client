from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ListDataSource(ClientValue):
    """Stores the parameters required for a list to communicate with its external data source."""

    Properties: Optional[dict] = None
