from __future__ import annotations

from dataclasses import field

from office365.directory.identitygovernance.quarantine_configuration import (
    QuarantineConfiguration,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class WorkflowSetting(ClientValue):
    quarantineConfiguration: QuarantineConfiguration = field(default_factory=QuarantineConfiguration)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.WorkflowSetting"
