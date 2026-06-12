from office365.entity_collection import EntityCollection
from office365.onenote.entity_hierarchy_model import OnenoteEntityHierarchyModel
from office365.onenote.sections.section import OnenoteSection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class Notebook(OnenoteEntityHierarchyModel):
    """A OneNote notebook."""

    @property
    def sections(self) -> EntityCollection[OnenoteSection]:
        """
        Retrieve a list of onenoteSection objects from the specified notebook.
        """
        return self.properties.get(
            "sections",
            EntityCollection(
                self.context,
                OnenoteSection,
                ResourcePath("sections", self.resource_path),
            ),
        )

    @odata(name="sectionGroups")
    @property
    def section_groups(self):
        """
        Retrieve a list of onenoteSection objects from the specified notebook.
        """

        from office365.onenote.sectiongroups.section_group import SectionGroup

        return self.properties.get(
            "sectionGroups",
            EntityCollection(
                self.context,
                SectionGroup,
                ResourcePath("sectionGroups", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self):
        return None  # type: ignore
