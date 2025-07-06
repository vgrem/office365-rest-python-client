from office365.entity import Entity


class CaseOperation(Entity):
    """An abstract entity that represents a long-running eDiscovery process.
    It contains a common set of properties that are shared among inheriting entities"""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.caseOperation"
