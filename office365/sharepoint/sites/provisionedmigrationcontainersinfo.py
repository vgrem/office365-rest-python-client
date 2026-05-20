from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ProvisionedMigrationContainersInfo(ClientValue):
    data_container_uri: Optional[str] = None
    encryption_key: Optional[bytes] = None
    metadata_container_uri: Optional[str] = None
