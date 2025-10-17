from typing import Optional

from office365.sharepoint.entity import Entity


class WorkflowDefinition(Entity):
    """Represents a workflow definition and associated properties."""

    @property
    def association_url(self) -> Optional[str]:
        """Gets the AssociationUrl property"""
        return self.properties.get("AssociationUrl", None)

    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the DisplayName property"""
        return self.properties.get("DisplayName", None)

    @property
    def draft_version(self) -> Optional[str]:
        """Gets the DraftVersion property"""
        return self.properties.get("DraftVersion", None)

    @property
    def form_field(self) -> Optional[str]:
        """Gets the FormField property"""
        return self.properties.get("FormField", None)

    @property
    def initiation_url(self) -> Optional[str]:
        """Gets the InitiationUrl property"""
        return self.properties.get("InitiationUrl", None)

    @property
    def properties(self) -> dict:
        """Gets the Properties property"""
        return self.properties.get("Properties", None)

    @property
    def published(self) -> Optional[bool]:
        """Gets the Published property"""
        return self.properties.get("Published", None)

    @property
    def requires_association_form(self) -> Optional[bool]:
        """Gets the RequiresAssociationForm property"""
        return self.properties.get("RequiresAssociationForm", None)

    @property
    def requires_initiation_form(self) -> Optional[bool]:
        """Gets the RequiresInitiationForm property"""
        return self.properties.get("RequiresInitiationForm", None)

    @property
    def restrict_to_scope(self) -> Optional[str]:
        """Gets the RestrictToScope property"""
        return self.properties.get("RestrictToScope", None)

    @property
    def restrict_to_type(self) -> Optional[str]:
        """Gets the RestrictToType property"""
        return self.properties.get("RestrictToType", None)

    @property
    def xaml(self) -> Optional[str]:
        """Gets the Xaml property"""
        return self.properties.get("Xaml", None)

    @property
    def entity_type_name(self):
        return "SP.WorkflowServices.WorkflowDefinition"
