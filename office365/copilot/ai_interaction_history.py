from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.copilot.ai_interaction import AiInteraction


class AiInteractionHistory(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AiInteractionHistory"

    @verb(role="action", effect="read")
    def get_all_enterprise_interactions(self) -> EntityCollection[AiInteraction]:
        """getAllEnterpriseInteractions operation."""
        from office365.copilot.ai_interaction import AiInteraction

        return_type = EntityCollection(self.context, AiInteraction)
        qry = FunctionQuery(self, "getAllEnterpriseInteractions", None, return_type)
        self.context.add_query(qry)
        return return_type
