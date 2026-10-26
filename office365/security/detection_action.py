from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.security.alerts.template import AlertTemplate
from office365.security.automated_action_set import AutomatedActionSet
from office365.security.organizational_scope import OrganizationalScope


@dataclass
class DetectionAction(ClientValue):
    alertTemplate: AlertTemplate = field(default_factory=AlertTemplate)
    automatedActions: AutomatedActionSet = field(default_factory=AutomatedActionSet)
    organizationalScope: OrganizationalScope = field(default_factory=OrganizationalScope)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.DetectionAction"
