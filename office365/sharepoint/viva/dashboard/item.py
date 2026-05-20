from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.paths.resource_path import ResourcePath


@dataclass
class DashboardItem(ClientValue):
    web_absolute_path: Optional[ResourcePath] = None
