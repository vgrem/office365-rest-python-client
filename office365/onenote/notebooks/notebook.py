from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity_collection import EntityCollection
from office365.onenote.entity_hierarchy_model import OnenoteEntityHierarchyModel
from office365.onenote.notebook_links import NotebookLinks
from office365.onenote.sections.collection import OnenoteSectionCollection
from office365.onenote.userrole import OnenoteUserRole
from office365.permissions import require_permission
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.onenote.operations.onenote import OnenoteOperation


class Notebook(OnenoteEntityHierarchyModel):
    """A OneNote notebook."""

    @odata(name="sections", navigation=True)
    @property
    def sections(self) -> OnenoteSectionCollection:
        """
        Retrieve a list of onenoteSection objects from the specified notebook.
        """
        return self.properties.get(
            "sections",
            OnenoteSectionCollection(
                self.context,
                ResourcePath("sections", self.resource_path),
            ),
        )

    @odata(name="sectionGroups", navigation=True)
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
    def entity_type_name(self) -> str:
        return None  # type: ignore

    @odata(name="isDefault")
    @property
    def is_default(self) -> Optional[bool]:
        """Gets the isDefault property"""
        return self.properties.get("isDefault", None)

    @odata(name="isShared")
    @property
    def is_shared(self) -> Optional[bool]:
        """Gets the isShared property"""
        return self.properties.get("isShared", None)

    @odata(name="links")
    @property
    def links(self) -> NotebookLinks:
        """Gets the links property"""
        return self.properties.get("links", NotebookLinks())

    @odata(name="sectionGroupsUrl")
    @property
    def section_groups_url(self) -> Optional[str]:
        """Gets the sectionGroupsUrl property"""
        return self.properties.get("sectionGroupsUrl", None)

    @odata(name="sectionsUrl")
    @property
    def sections_url(self) -> Optional[str]:
        """Gets the sectionsUrl property"""
        return self.properties.get("sectionsUrl", None)

    @odata(name="userRole")
    @property
    def user_role(self) -> OnenoteUserRole:
        """Gets the userRole property"""
        return self.properties.get("userRole", OnenoteUserRole.Unknown)

    @require_permission(
        delegated=["Notes.Create", "Notes.ReadWrite", "Notes.ReadWrite.All"],
        application=["Notes.ReadWrite.All"],
    )
    def copy_notebook(
        self, group_id: str, rename_as: str, notebook_folder: str, site_collection_id: str, site_id: str
    ) -> OnenoteOperation:
        """copyNotebook operation.

        Args:
            group_id (str):
                groupId parameter
            rename_as (str):
                renameAs parameter
            notebook_folder (str):
                notebookFolder parameter
            site_collection_id (str):
                siteCollectionId parameter
            site_id (str):
                siteId parameter
        """
        from office365.onenote.operations.onenote import OnenoteOperation

        return_type = OnenoteOperation(self.context)
        qry = ServiceOperationQuery(
            self,
            "copyNotebook",
            None,
            {
                "groupId": group_id,
                "renameAs": rename_as,
                "notebookFolder": notebook_folder,
                "siteCollectionId": site_collection_id,
                "siteId": site_id,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
