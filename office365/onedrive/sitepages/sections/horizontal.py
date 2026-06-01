from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.sitepages.horizontalsectionlayouttype import HorizontalSectionLayoutType
from office365.onedrive.sitepages.sectionemphasistype import SectionEmphasisType
from office365.onedrive.sitepages.sections.horizontal_column import HorizontalSectionColumn
from office365.runtime.paths.resource_path import ResourcePath


class HorizontalSection(Entity):
    """Represents a horizontal section in a given SharePoint page."""

    @property
    def columns(self) -> EntityCollection[HorizontalSectionColumn]:
        """The set of vertical columns in this section."""
        return self.properties.get(
            "columns",
            EntityCollection(self.context, HorizontalSectionColumn, ResourcePath("columns", self.resource_path)),
        )

    @property
    def emphasis(self) -> SectionEmphasisType:
        """Gets the emphasis property"""
        return self.properties.get("emphasis", SectionEmphasisType.none)

    @property
    def layout(self) -> HorizontalSectionLayoutType:
        """Gets the layout property"""
        return self.properties.get("layout", HorizontalSectionLayoutType.none)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.HorizontalSection"
