from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.sitepages.sections.horizontal import HorizontalSection
from office365.onedrive.sitepages.sections.vertical import VerticalSection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class CanvasLayout(Entity):
    """Represents the layout of the content in a given SharePoint page."""

    @odata(name="horizontalSections")
    @property
    def horizontal_sections(self) -> EntityCollection[HorizontalSection]:
        """Collection of horizontal sections on the SharePoint page."""
        return self.properties.get(
            "horizontalSections",
            EntityCollection(self.context, HorizontalSection, ResourcePath("horizontalSections", self.resource_path)),
        )

    @odata(name="verticalSection")
    @property
    def vertical_section(self) -> VerticalSection:
        """Vertical section on the SharePoint page."""
        return self.properties.get(
            "verticalSection", VerticalSection(self.context, ResourcePath("verticalSection", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CanvasLayout"
