from office365.entity import Entity
from office365.entity_collection import EntityCollection


class IdentityUserFlowAttributeAssignment(Entity):
    """Update the properties of a identityUserFlowAttributeAssignment object."""


class IdentityUserFlowAttributeAssignmentCollection(EntityCollection):
    def __init__(self, context, resource_path=None):
        super().__init__(context, IdentityUserFlowAttributeAssignment, resource_path)
