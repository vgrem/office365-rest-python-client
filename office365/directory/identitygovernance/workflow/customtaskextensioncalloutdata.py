from __future__ import annotations
from office365.directory.users.user import User
from office365.runtime.client_value import ClientValue
from dataclasses import dataclass, field
from office365.runtime.paths.resource_path import ResourcePath

class CustomTaskExtensionCalloutData(ClientValue):
    subject: User | None = None
    task: Task | None = None
    taskProcessingresult: TaskProcessingResult | None = None
    workflow: Workflow | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.identityGovernance.CustomTaskExtensionCalloutData'