from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity_collection import EntityCollection
from office365.intune.servicecommunications.announcement_base import (
    ServiceAnnouncementBase,
)
from office365.intune.servicecommunications.service_update_message_viewpoint import ServiceUpdateMessageViewpoint
from office365.intune.servicecommunications.updatecategory import ServiceUpdateCategory
from office365.intune.servicecommunications.updateseverity import ServiceUpdateSeverity
from office365.outlook.mail.item_body import ItemBody
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.common.service_announcement_attachment import (
        ServiceAnnouncementAttachment,
    )


class ServiceUpdateMessage(ServiceAnnouncementBase):
    """
    Represents the announcements about changes in a service.

    Represents announcements such as major updates, new features in a product;
    for example, the publication of a new SharePoint feature.
    """

    @odata(name="actionRequiredByDateTime")
    @property
    def action_required_by_date_time(self) -> Optional[datetime]:
        """Gets the actionRequiredByDateTime property"""
        return self.properties.get("actionRequiredByDateTime", datetime.min)

    @odata(name="attachmentsArchive")
    @property
    def attachments_archive(self) -> Optional[bytes]:
        """Gets the attachmentsArchive property"""
        return self.properties.get("attachmentsArchive", None)

    @odata(name="body")
    @property
    def body(self) -> ItemBody:
        """Gets the body property"""
        return self.properties.get("body", ItemBody())

    @odata(name="category")
    @property
    def category(self) -> ServiceUpdateCategory:
        """Gets the category property"""
        return self.properties.get("category", ServiceUpdateCategory.preventOrFixIssue)

    @odata(name="hasAttachments")
    @property
    def has_attachments(self) -> Optional[bool]:
        """Gets the hasAttachments property"""
        return self.properties.get("hasAttachments", None)

    @odata(name="isMajorChange")
    @property
    def is_major_change(self) -> Optional[bool]:
        """Gets the isMajorChange property"""
        return self.properties.get("isMajorChange", None)

    @odata(name="services")
    @property
    def services(self) -> StringCollection:
        """Gets the services property"""
        return self.properties.get("services", StringCollection())

    @odata(name="severity")
    @property
    def severity(self) -> ServiceUpdateSeverity:
        """Gets the severity property"""
        return self.properties.get("severity", ServiceUpdateSeverity.normal)

    @odata(name="tags")
    @property
    def tags(self) -> StringCollection:
        """Gets the tags property"""
        return self.properties.get("tags", StringCollection())

    @odata(name="viewPoint")
    @property
    def view_point(self) -> ServiceUpdateMessageViewpoint:
        """Gets the viewPoint property"""
        return self.properties.get("viewPoint", ServiceUpdateMessageViewpoint())

    @odata(name="attachments", navigation=True)
    @property
    def attachments(self) -> EntityCollection[ServiceAnnouncementAttachment]:
        """Gets the attachments property"""
        from office365.common.service_announcement_attachment import (
            ServiceAnnouncementAttachment,
        )

        return self.properties.get(
            "attachments",
            EntityCollection[ServiceAnnouncementAttachment](
                self.context, ServiceAnnouncementAttachment, ResourcePath("attachments", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ServiceUpdateMessage"
