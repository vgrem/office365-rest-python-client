from typing import Optional
from uuid import UUID

from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class WorkflowSubscription(Entity):

    @property
    def definition_id(self) -> Optional[UUID]:
        """Gets the DefinitionId property"""
        return self.properties.get("DefinitionId", None)

    @property
    def enabled(self) -> Optional[bool]:
        """Gets the Enabled property"""
        return self.properties.get("Enabled", None)

    @property
    def event_source_id(self) -> Optional[UUID]:
        """Gets the EventSourceId property"""
        return self.properties.get("EventSourceId", None)

    @property
    def event_types(self) -> StringCollection:
        """Gets the EventTypes property"""
        return self.properties.get("EventTypes", None)

    @property
    def manual_start_bypasses_activation_limit(self) -> Optional[bool]:
        """Gets the ManualStartBypassesActivationLimit property"""
        return self.properties.get("ManualStartBypassesActivationLimit", None)

    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def parent_content_type_id(self) -> Optional[str]:
        """Gets the ParentContentTypeId property"""
        return self.properties.get("ParentContentTypeId", None)

    @property
    def property_definitions(self) -> dict:
        """Gets the PropertyDefinitions property"""
        return self.properties.get("PropertyDefinitions", None)

    @property
    def status_field_name(self) -> Optional[str]:
        """Gets the StatusFieldName property"""
        return self.properties.get("StatusFieldName", None)

    @property
    def entity_type_name(self):
        return "SP.WorkflowServices.WorkflowSubscription"
