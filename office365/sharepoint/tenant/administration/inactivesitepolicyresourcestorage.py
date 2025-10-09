from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.fields.lookup_value import FieldLookupValue


class InactiveSitePolicyResourceStorage(ClientValue):

    def __init__(
        self,
        created_on: datetime = None,
        last_scoped_on: datetime = None,
        last_transitioned_on: datetime = None,
        lookup_site_id: FieldLookupValue = FieldLookupValue(),
        notification_data: str = None,
        notification_status: int = None,
        resource_id: str = None,
        resource_state: int = None,
        resource_state_transition_data: str = None,
        resource_type: int = None,
        updated_on: datetime = None,
        user_responses: str = None,
    ):
        self.createdOn = created_on
        self.lastScopedOn = last_scoped_on
        self.lastTransitionedOn = last_transitioned_on
        self.lookupSiteId = lookup_site_id
        self.notificationData = notification_data
        self.notificationStatus = notification_status
        self.resourceId = resource_id
        self.resourceState = resource_state
        self.resourceStateTransitionData = resource_state_transition_data
        self.resourceType = resource_type
        self.updatedOn = updated_on
        self.userResponses = user_responses

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.InactiveSitePolicyResourceStorage"
