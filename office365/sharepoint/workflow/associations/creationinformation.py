from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class WorkflowAssociationCreationInformation(ClientValue):
    ContentTypeAssociationHistoryListName: Optional[str] = None
    ContentTypeAssociationTaskListName: Optional[str] = None
    Name: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Workflow.WorkflowAssociationCreationInformation"
