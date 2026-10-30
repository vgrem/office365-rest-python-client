from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.directory.policies.conditionalaccess.templatescenarios import TemplateScenarios
from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.policies.conditionalaccess.policy_detail import (
        ConditionalAccessPolicyDetail,
    )


class ConditionalAccessTemplate(Entity):
    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="details")
    @property
    def details(self) -> ConditionalAccessPolicyDetail:
        """Gets the details property"""
        from office365.directory.policies.conditionalaccess.policy_detail import (
            ConditionalAccessPolicyDetail,
        )

        return self.properties.get("details", ConditionalAccessPolicyDetail())

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="scenarios")
    @property
    def scenarios(self) -> TemplateScenarios:
        """Gets the scenarios property"""
        return self.properties.get("scenarios", TemplateScenarios.new)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessTemplate"
