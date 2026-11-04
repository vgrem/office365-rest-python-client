from dataclasses import field
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class BatchUpdatePayload(ClientValue):
    Tags: StringCollection = field(default_factory=StringCollection)
    TaskId: Optional[UUID] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.BatchUpdatePayload"
