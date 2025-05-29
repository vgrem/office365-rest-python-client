from office365.runtime.client_value import ClientValue


class CopyMigrationInfo(ClientValue):
    """"""

    def __init__(
        self,
        encryption_key=None,
        job_id=None,
        job_queue_uri=None,
        source_list_item_unique_ids=None,
    ):
        self.EncryptionKey = encryption_key
        self.JobId = job_id
        self.JobQueueUri = job_queue_uri
        self.SourceListItemUniqueIds = source_list_item_unique_ids
