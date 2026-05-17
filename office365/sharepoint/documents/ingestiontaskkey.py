from typing import Optional

from office365.runtime.client_value import ClientValue


class IngestionTaskKey(ClientValue):
    def __init__(
        self,
        ingestion_table_account_key: Optional[str] = None,
        ingestion_table_account_name: Optional[str] = None,
        job_id: Optional[str] = None,
        task_id: Optional[str] = None,
        tenant_name: Optional[str] = None,
    ):
        self.ingestion_table_account_key = ingestion_table_account_key
        self.ingestion_table_account_name = ingestion_table_account_name
        self.job_id = job_id
        self.task_id = task_id
        self.tenant_name = tenant_name
