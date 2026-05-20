from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class IngestionTaskKey(ClientValue):
    ingestion_table_account_key: Optional[str] = None
    ingestion_table_account_name: Optional[str] = None
    job_id: Optional[str] = None
    task_id: Optional[str] = None
    tenant_name: Optional[str] = None
