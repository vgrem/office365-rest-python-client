from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class BatchUpdatePayload(ClientValue):

    def __init__(
        self, tags: StringCollection = StringCollection(), task_id: UUID = None
    ):
        self.Tags = tags
        self.TaskId = task_id

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.BatchUpdatePayload"
