from typing import List

from typing_extensions import Self

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.translation.notifications.recipient_col import (
    TranslationNotificationRecipientCollection,
)
from office365.sharepoint.translation.notifications.recipient_set_request import (
    TranslationNotificationRecipientSetRequest,
)
from office365.sharepoint.translation.notifications.recipient_users import (
    TranslationNotificationRecipientUsers,
)


class MultilingualSettings(Entity):
    """ """

    def set_notification_recipients(
        self, notification_recipients: List[TranslationNotificationRecipientCollection]
    ) -> Self:
        """
        :param list notification_recipients:
        """
        request = TranslationNotificationRecipientSetRequest(notification_recipients)
        qry = ServiceOperationQuery(self, "SetNotificationRecipients", None, request)
        self.context.add_query(qry)
        return self

    @property
    def recipients(self) -> EntityCollection[TranslationNotificationRecipientUsers]:
        return self.properties.get(
            "Recipients",
            EntityCollection(
                self.context,
                TranslationNotificationRecipientUsers,
                ResourcePath("Recipients", self.resource_path),
            ),
        )
