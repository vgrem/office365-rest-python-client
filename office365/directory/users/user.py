from __future__ import annotations

import json
from datetime import datetime
from typing import Any, List, Optional, Union

from typing_extensions import Self

from office365.communications.onlinemeetings.collection import OnlineMeetingCollection
from office365.communications.presences.presence import Presence
from office365.delta_collection import DeltaCollection
from office365.directory.applications.roles.assignment_collection import (
    AppRoleAssignmentCollection,
)
from office365.directory.audit.signins.activity import SignInActivity
from office365.directory.authentication.authentication import Authentication
from office365.directory.extensions.extension import Extension
from office365.directory.extensions.open_type import OpenTypeExtension
from office365.directory.identities.object_identity import ObjectIdentity
from office365.directory.identitygovernance.termsofuse.agreement_acceptance import (
    AgreementAcceptance,
)
from office365.directory.insights.office_graph import OfficeGraphInsights
from office365.directory.licenses.assigned_license import AssignedLicense
from office365.directory.licenses.assigned_plan import AssignedPlan
from office365.directory.licenses.assignment_state import LicenseAssignmentState
from office365.directory.licenses.details import LicenseDetails
from office365.directory.objects.collection import DirectoryObjectCollection
from office365.directory.objects.object import DirectoryObject
from office365.directory.permissions.grants.oauth2 import OAuth2PermissionGrant
from office365.directory.profile_photo import ProfilePhoto
from office365.directory.rolemanagement.role import DirectoryRole
from office365.directory.users.activities.collection import UserActivityCollection
from office365.directory.users.password_profile import PasswordProfile
from office365.directory.users.settings import UserSettings
from office365.entity_collection import EntityCollection
from office365.intune.devices.data import DeviceAndAppManagementData
from office365.intune.devices.management.managed.app.diagnostic_status import (
    ManagedAppDiagnosticStatus,
)
from office365.intune.devices.management.managed.managed import ManagedDevice
from office365.intune.organizations.contact import OrgContact
from office365.intune.policies.managed_app import ManagedAppPolicy
from office365.onedrive.drives.drive import Drive
from office365.onedrive.sites.site import Site
from office365.onenote.onenote import Onenote
from office365.outlook.calendar.attendees.base import AttendeeBase
from office365.outlook.calendar.calendar import Calendar
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.calendar.events.event import Event
from office365.outlook.calendar.events.reminder import Reminder
from office365.outlook.calendar.group import CalendarGroup
from office365.outlook.calendar.location_constraint import LocationConstraint
from office365.outlook.calendar.meetingtimes.suggestions_result import (
    MeetingTimeSuggestionsResult,
)
from office365.outlook.calendar.meetingtimes.time_constraint import TimeConstraint
from office365.outlook.contacts.collection import ContactCollection
from office365.outlook.contacts.folder import ContactFolder
from office365.outlook.convert_id_result import ConvertIdResult
from office365.outlook.exchangeidformat import ExchangeIdFormat
from office365.outlook.mail.folders.collection import MailFolderCollection
from office365.outlook.mail.item_body import ItemBody
from office365.outlook.mail.mailbox_settings import MailboxSettings
from office365.outlook.mail.messages.collection import MessageCollection
from office365.outlook.mail.messages.message import Message
from office365.outlook.mail.recipient import Recipient
from office365.outlook.mail.tips.tips import MailTips
from office365.outlook.person import Person
from office365.outlook.user import OutlookUser
from office365.planner.user import PlannerUser
from office365.runtime.client_object_meta import persist_property
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v4.entity import EntityPath
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.teams.chats.collection import ChatCollection
from office365.teams.collection import TeamCollection
from office365.teams.teamwork.shiftmanagement.user_solution_root import UserSolutionRoot
from office365.teams.teamwork.user import UserTeamwork
from office365.teams.viva.employee_experience_user import EmployeeExperienceUser
from office365.todo.todo import Todo


class User(DirectoryObject):
    """Represents an Azure AD user account. Inherits from directoryObject."""

    def __repr__(self):
        return self.user_principal_name or self.id or self.entity_type_name

    def enable_automatic_replies_setting(
        self,
        status: str,
        scheduled_start_datetime: datetime,
        scheduled_end_datetime: datetime,
        internal_reply_message: str = None,
        external_reply_message: str = None,
    ) -> Self:
        """
        Enable, configure, automatic replies (notify people automatically upon receipt of their email)

        """
        from office365.outlook.mail.automaticreplies.setting import (
            AutomaticRepliesSetting,
        )

        setting = AutomaticRepliesSetting(
            status=status,
            scheduled_start_datetime=DateTimeTimeZone.parse(scheduled_start_datetime),
            scheduled_end_datetime=DateTimeTimeZone.parse(scheduled_end_datetime),
            internal_reply_message=internal_reply_message,
            external_reply_message=external_reply_message,
        )

        def _construct_request(request):
            payload = {"automaticRepliesSetting": setting.to_json()}
            request.data = payload
            request.url += "/mailboxSettings"

        self.update().before_execute(_construct_request)
        return self

    def disable_automatic_replies_setting(self, clear_all=False) -> Self:
        """
        Disable automatic replies (notify people automatically upon receipt of their email)
        :param bool clear_all: If true, clear all automatic replies settings
        """
        from office365.outlook.mail.automaticreplies.setting import (
            AutomaticRepliesSetting,
        )

        setting = AutomaticRepliesSetting(
            status="disabled",
        )

        def _construct_request(request):
            payload = {"automaticRepliesSetting": setting.to_json()}
            request.data = payload
            request.url += "/mailboxSettings"

        self.update().before_execute(_construct_request)
        return self

    def add_extension(self, name: str) -> OpenTypeExtension:
        """
        Creates an open extension (openTypeExtension object) and add custom properties in a new or existing instance
        of a User resource.
        :param str name:
        """
        from office365.directory.extensions.open_type import OpenTypeExtension

        return_type = OpenTypeExtension(self.context)
        return_type.set_property("extensionName", name)
        self.extensions.add_child(return_type)
        qry = CreateEntityQuery(self.extensions, return_type, return_type)
        self.context.add_query(qry)
        return return_type

    def assign_license(self, add_licenses: List[str], remove_licenses: List[str]) -> Self:
        """
        Add or remove licenses on the user.

        :param list[str] remove_licenses: A collection of skuIds that identify the licenses to remove.
        :param list[AssignedLicense] add_licenses: A collection of assignedLicense objects that specify
             the licenses to add.
        """
        params = {
            "addLicenses": ClientValueCollection(AssignedLicense, add_licenses),
            "removeLicenses": StringCollection(remove_licenses),
        }
        qry = ServiceOperationQuery(self, "assignLicense", None, params, None, self)
        self.context.add_query(qry)
        return self

    def assign_manager(self, user: Union[str, User, OrgContact]):
        """
        Assign a user's manager.

        :param str or User or OrgContact user: User or office365.intune.organizations.contact.OrgContact
            or identifier
        """

        def _construct_request(request: RequestOptions) -> None:
            request.method = HttpMethod.Put
            request.set_header("Content-Type", "application/json")
            request.set_header("Accept", "application/json")
            request.data = json.dumps(request.data)

        def _assign_manager(user_id: str) -> None:
            payload = {"@odata.id": f"https://graph.microsoft.com/v1.0/users/{user_id}"}
            qry = ServiceOperationQuery(self.manager, "$ref", None, payload)
            self.context.add_query(qry).before_query_execute(_construct_request)

        if isinstance(user, User):

            def _user_loaded():
                _assign_manager(user.id)

            user.ensure_property("id", _user_loaded)
        else:
            _assign_manager(user)
        return self.manager

    def remove_manager(self) -> Self:
        """Remove a user's manager."""
        qry = ServiceOperationQuery(self.manager, "$ref")

        def _construct_request(request: RequestOptions) -> None:
            request.method = HttpMethod.Delete

        self.context.add_query(qry).before_query_execute(_construct_request)
        return self

    def change_password(self, current_password: str, new_password: str) -> Self:
        """
        Enable the user to update their password. Any user can update their password without belonging
        to any administrator role.

        :param str current_password: Your current password.
        :param str new_password: Your new password.
        """
        qry = ServiceOperationQuery(
            self,
            "changePassword",
            None,
            {"currentPassword": current_password, "newPassword": new_password},
        )
        self.context.add_query(qry)
        return self

    def follow_site(self, site: Union[str, Site]) -> Self:
        """follow a site"""

        def _follow_site(site_id: str) -> None:
            payload = {
                "value": [
                    {
                        "id": site_id,
                    }
                ]
            }
            query = ServiceOperationQuery(self.followed_sites, "add", None, payload)
            self.context.add_query(query)

        if isinstance(site, Site):

            def _user_loaded():
                _follow_site(site.id)

            site.ensure_property("id", _user_loaded)
        else:
            _follow_site(site)
        return self

    def unfollow_site(self, site: Union[str, Site]) -> Self:
        """Unfollow a user's site or multiple sites."""

        def _unfollow_site(site_id: str) -> None:
            payload = {
                "value": [
                    {
                        "id": site_id,
                    }
                ]
            }
            query = ServiceOperationQuery(self.followed_sites, "remove", None, payload)
            self.context.add_query(query)

        if isinstance(site, Site):

            def _user_loaded():
                _unfollow_site(site.id)

            site.ensure_property("id", _user_loaded)
        else:
            _unfollow_site(site)

        return self

    def get_directory_roles(self) -> EntityCollection[DirectoryRole]:
        """
        Fetches all directory roles assigned to the user.

        Returns:
            EntityCollection[DirectoryRole]: The directory roles the user is a member of.

        Docs:
            https://learn.microsoft.com/en-us/graph/api/directoryrole-list?view=graph-rest-1.0
        """
        return_type = EntityCollection(self.context, DirectoryRole)

        def _directory_roles_loaded(directory_roles: List[DirectoryRole]):
            role_template_map = {role.role_template_id: role for role in directory_roles}

            def _memberships_loaded(memberships: DirectoryObjectCollection):
                for item in memberships:
                    role_id = item.properties.get("roleTemplateId")
                    if role_id in role_template_map:
                        return_type.add_child(role_template_map[role_id])

            self.member_of.get().after_execute(_memberships_loaded)

        self.context.directory_roles.get().after_execute(_directory_roles_loaded)

        return return_type

    def get_mail_tips(
        self, email_addresses: List[str], mail_tips_options: str = None
    ) -> ClientResult[ClientValueCollection[MailTips]]:
        """Get the MailTips of one or more recipients as available to the signed-in user.
        :param list[str] email_addresses: A collection of SMTP addresses of recipients to get MailTips for.
        :param str mail_tips_options: A enumeration of flags that represents the requested mailtips.
            Possible values are: automaticReplies, customMailTip, deliveryRestriction, externalMemberCount,
            mailboxFullStatus, maxMessageSize, moderationStatus, recipientScope, recipientSuggestions,
            and totalMemberCount.
        """
        return_type = ClientResult(self.context, ClientValueCollection(MailTips))
        payload = {
            "EmailAddresses": StringCollection(email_addresses),
            "MailTipsOptions": mail_tips_options,
        }
        qry = ServiceOperationQuery(
            self,
            "getMailTips",
            None,
            payload,
        )
        self.context.add_query(qry)
        return return_type

    def get_my_site(self) -> Site:
        """Gets user's site"""
        return_type = Site(self.context)

        def _loaded():
            return_type.set_property("webUrl", self.my_site)

        self.ensure_property("mySite", _loaded)
        return return_type

    def send_mail(
        self,
        subject: str,
        body: Union[str, ItemBody],
        to_recipients: List[str],
        cc_recipients: List[str] = None,
        bcc_recipients: List[str] = None,
        reply_to: List[str] = None,
        save_to_sent_items: bool = False,
        body_type: str = "Text",
    ) -> Message:
        """Send a new message on the fly

        :param str subject: The subject of the message.
        :param str body: The body of the message. It can be in HTML or text format
        :param list[str] to_recipients: The To: recipients for the message.
        :param list[str] cc_recipients: The CC: recipients for the message.
        :param list[str] bcc_recipients: The BCC: recipients for the message.
        :param list[str] reply_to: The Reply-To: : recipients for the reply to the message.
        :param bool save_to_sent_items: Indicates whether to save the message in Sent Items. Specify it only if
            the parameter is false; default is true
        :param str body_type: The type of the message body. It can be "HTML" or "Text". Default is "Text".
        """
        return_type = Message(self.context)
        return_type.subject = subject
        return_type.body = (body, body_type)
        [return_type.to_recipients.add(Recipient.from_email(email)) for email in to_recipients]
        if bcc_recipients is not None:
            [return_type.bcc_recipients.add(Recipient.from_email(email)) for email in bcc_recipients]
        if cc_recipients is not None:
            [return_type.cc_recipients.add(Recipient.from_email(email)) for email in cc_recipients]
        if reply_to is not None:
            [return_type.reply_to.add(Recipient.from_email(email)) for email in reply_to]

        payload = {"message": return_type, "saveToSentItems": save_to_sent_items}
        qry = ServiceOperationQuery(self, "sendmail", None, payload)
        self.context.add_query(qry)
        return return_type

    def export_personal_data(self, storage_location) -> Self:
        """
        Submit a data policy operation request from a company administrator or an application to
        export an organizational user's data.

        If successful, this method returns a 202 Accepted response code.
        It does not return anything in the response body. The response contains the following response headers.

        :param str storage_location: This is a shared access signature (SAS) URL to an Azure Storage account,
            to where data should be exported.
        """
        qry = ServiceOperationQuery(self, "exportPersonalData", None, {"storage_location": storage_location})
        self.context.add_query(qry)
        return self

    def export_device_and_app_management_data(
        self,
    ) -> ClientResult[ClientValueCollection[DeviceAndAppManagementData]]:
        """"""
        return_type = ClientResult(self.context, ClientValueCollection(DeviceAndAppManagementData))
        qry = FunctionQuery(self, "exportDeviceAndAppManagementData", None, return_type)
        self.context.add_query(qry)
        return return_type

    def find_meeting_times(
        self,
        attendees: List[AttendeeBase] = None,
        location_constraint: LocationConstraint = None,
        time_constraint: TimeConstraint = None,
        meeting_duration: str = None,
        max_candidates: int = None,
        is_organizer_optional=None,
        return_suggestion_reasons=None,
        minimum_attendee_percentage=None,
    ) -> ClientResult[MeetingTimeSuggestionsResult]:
        """
        Suggest meeting times and locations based on organizer and attendees availability, and time or location
        constraints specified as parameters.

        If findMeetingTimes cannot return any meeting suggestions, the response would indicate a reason in the
        emptySuggestionsReason property. Based on this value, you can better adjust the parameters
        and call findMeetingTimes again.

        The algorithm used to suggest meeting times and locations undergoes fine-tuning from time to time.
        In scenarios like test environments where the input parameters and calendar data remain static, expect
        that the suggested results may differ over time.

        :param list[AttendeeBase] or None attendees: A collection of attendees or resources for the meeting.
            Since findMeetingTimes assumes that any attendees who is a person is always required, specify required
            for a person and resource for a resource in the corresponding type property. An empty collection causes
            findMeetingTimes to look for free time slots for only the organizer. Optional.
        :param office365.outlook.calendar.location_constraint.LocationConstraint or None location_constraint:
            The organizer's requirements about the meeting location, such as whether a suggestion for a meeting
            location is required, or there are specific locations only where the meeting can take place. Optional.
        :param TimeConstraint time_constraint: Any time restrictions for a meeting, which can include the nature
            of the meeting (activityDomain property) and possible meeting time periods (timeSlots property).
            findMeetingTimes assumes activityDomain as work if you don't specify this parameter. Optional.
        :param str meeting_duration: The length of the meeting, denoted in ISO8601 format.
             For example, 1 hour is denoted as 'PT1H', where 'P' is the duration designator,
             'T' is the time designator, and 'H' is the hour designator.
             Use M to indicate minutes for the duration; for example, 2 hours and 30 minutes would be 'PT2H30M'.
             If no meeting duration is specified, findMeetingTimes uses the default of 30 minutes. Optional.
        :param int max_candidates: The maximum number of meeting time suggestions to be returned. Optional.
        :param bool is_organizer_optional: Specify True if the organizer doesn't necessarily have to attend.
             The default is false. Optiona
        :param bool return_suggestion_reasons: Specify True to return a reason for each meeting suggestion in
             the suggestionReason property. The default is false to not return that property. Optional.
        :param float minimum_attendee_percentage: The minimum required confidence for a time slot to be returned
            in the response. It is a % value ranging from 0 to 100. Optional.
        """
        payload = {
            "attendees": ClientValueCollection(AttendeeBase, attendees),
            "locationConstraint": location_constraint,
            "timeConstraint": time_constraint,
            "meeting_duration": meeting_duration,
            "maxCandidates": max_candidates,
            "isOrganizerOptional": is_organizer_optional,
            "returnSuggestionReasons": return_suggestion_reasons,
            "minimumAttendeePercentage": minimum_attendee_percentage,
        }
        return_type = ClientResult(self.context, MeetingTimeSuggestionsResult())
        qry = ServiceOperationQuery(self, "findMeetingTimes", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_calendar_view(self, start_dt: datetime, end_dt: datetime) -> EntityCollection[Event]:
        """Get the occurrences, exceptions, and single instances of events in a calendar view defined by a time range,
           from the user's default calendar, or from some other calendar of the user's.

        :param datetime.datetime end_dt: The end date and time of the time range, represented in ISO 8601 format.
             For example, "2019-11-08T20:00:00-08:00".
        :param datetime.datetime start_dt: The start date and time of the time range, represented in ISO 8601 format.
            For example, "2019-11-08T19:00:00-08:00".

        """
        return_type = EntityCollection(self.context, Event, ResourcePath("calendarView", self.resource_path))
        qry = ServiceOperationQuery(self, "calendarView", None, None, None, return_type)

        def _construct_request(request: RequestOptions) -> None:
            request.method = HttpMethod.Get
            request.url += f"?startDateTime={start_dt.isoformat()}&endDateTime={end_dt.isoformat()}"

        self.context.add_query(qry).before_query_execute(_construct_request)
        return return_type

    def get_reminder_view(self, start_dt: datetime, end_dt: datetime) -> ClientResult[ClientValueCollection[Reminder]]:
        """Get the occurrences, exceptions, and single instances of events in a calendar view defined by a time range,
                   from the user's default calendar, or from some other calendar of the user's.

        :param datetime.datetime end_dt: The end date and time of the event for which the reminder is set up.
            The value is represented in ISO 8601 format, for example, "2015-11-08T20:00:00.0000000"..
        :param datetime.datetime start_dt: The start date and time of the event for which the reminder is set up.
            The value is represented in ISO 8601 format, for example, "2015-11-08T19:00:00.0000000".
        """
        return_type = ClientResult(self.context, ClientValueCollection(Reminder))
        params = {
            "startDateTime": start_dt.isoformat(),
            "endDateTime": end_dt.isoformat(),
        }
        qry = FunctionQuery(self, "reminderView", params, return_type)
        self.context.add_query(qry)
        return return_type

    def get_managed_app_diagnostic_statuses(
        self,
    ) -> ClientResult[ClientValueCollection[ManagedAppDiagnosticStatus]]:
        """Gets diagnostics validation status for a given user."""
        return_type = ClientResult(self.context, ClientValueCollection(ManagedAppDiagnosticStatus))
        qry = FunctionQuery(self, "getManagedAppDiagnosticStatuses", None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_managed_app_policies(self) -> EntityCollection[ManagedAppPolicy]:
        """Gets app restrictions for a given user."""
        return_type = EntityCollection(self.context, ManagedAppPolicy)
        qry = FunctionQuery(self, "getManagedAppPolicies", None, return_type)
        self.context.add_query(qry)
        return return_type

    def delete_object(self, permanent_delete: bool = False) -> Self:
        """
        :param permanent_delete: Permanently deletes the user from directory
        :type permanent_delete: bool
        """
        super().delete_object()
        if permanent_delete:
            deleted_user = self.context.directory.deleted_users[self.id]
            deleted_user.delete_object()
        return self

    def revoke_signin_sessions(self) -> ClientResult[bool]:
        """
        Invalidates all the refresh tokens issued to applications for a user
        (as well as session cookies in a user's browser), by resetting the signInSessionsValidFromDateTime user
        property to the current date-time. Typically, this operation is performed (by the user or an administrator)
        if the user has a lost or stolen device. This operation prevents access to the organization's data through
        applications on the device by requiring the user to sign in again to all applications that they have previously
        consented to, independent of device.
        """
        result = ClientResult(self.context)
        qry = ServiceOperationQuery(self, "revokeSignInSessions", None, None, None, result)
        self.context.add_query(qry)
        return result

    def reprocess_license_assignment(self) -> User:
        """
        Reprocess all group-based license assignments for the user. To learn more about group-based licensing,
        see What is group-based licensing in Azure Active Directory. Also see Identify and resolve license assignment
        problems for a group in Azure Active Directory for more details.
        """
        return_type = User(self.context)
        qry = ServiceOperationQuery(self, "reprocessLicenseAssignment", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def remove_all_devices_from_management(self) -> Self:
        """
        Retire all devices from management for this user
        """
        qry = ServiceOperationQuery(self, "removeAllDevicesFromManagement")
        self.context.add_query(qry)
        return self

    def wipe_managed_app_registrations_by_device_tag(self, device_tag: str) -> Self:
        """
        Issues a wipe operation on an app registration with specified device tag.
        :param str device_tag: device tag
        """
        payload = {"deviceTag": device_tag}
        qry = ServiceOperationQuery(self, "wipeManagedAppRegistrationsByDeviceTag", None, payload)
        self.context.add_query(qry)
        return self

    def translate_exchange_ids(
        self,
        input_ids: List[str],
        source_id_type: ExchangeIdFormat = None,
        target_id_type: ExchangeIdFormat = None,
    ) -> ClientResult[ConvertIdResult]:
        """
        Translate identifiers of Outlook-related resources between formats.

        :param list[str] input_ids: A collection of identifiers to convert. All identifiers in the collection MUST
            have the same source ID type, and MUST be for items in the same mailbox. Maximum size of this collection
            is 1000 strings.
        :param str source_id_type: The ID type of the identifiers in the InputIds parameter.
        :param str target_id_type: The requested ID type to convert to.
        """
        return_type = ClientResult(self.context, ConvertIdResult())
        payload = {
            "InputIds": StringCollection(input_ids),
            "TargetIdType": target_id_type.name if target_id_type else None,
            "SourceIdType": source_id_type.name if source_id_type else None,
        }
        qry = ServiceOperationQuery(self, "translateExchangeIds", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def created_datetime(self) -> Optional[datetime]:
        """
        The Timestamp type represents date and time information using ISO 8601 format and is always in UTC time.
        For example, midnight UTC on Jan 1, 2014 is 2014-01-01T00:00:00Z
        """
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def last_password_change_datetime(self) -> Optional[datetime]:
        """
        The time when this Azure AD user last changed their password.
        """
        return self.properties.get("lastPasswordChangeDateTime", datetime.min)

    @property
    def created_objects(self) -> DirectoryObjectCollection:
        """Directory objects created by this user."""
        return self.properties.get(
            "createdObjects",
            DirectoryObjectCollection(self.context, ResourcePath("createdObjects", self.resource_path)),
        )

    @property
    def device_enrollment_limit(self) -> Optional[str]:
        """ """
        return self.properties.get("deviceEnrollmentLimit", None)

    @property
    def sign_in_activity(self):
        """Get the last signed-in date and request ID of the sign-in for a given user. Read-only."""
        return self.properties.get("signInActivity", SignInActivity())

    @property
    def account_enabled(self) -> Optional[bool]:
        """True if the account is enabled; otherwise, false. This property is required when a user is created."""
        return self.properties.get("accountEnabled", None)

    @property
    def age_group(self) -> Optional[str]:
        """Gets the age group of the user"""
        return self.properties.get("ageGroup", None)

    @property
    def app_role_assignments(self) -> AppRoleAssignmentCollection:
        """Get the apps and app roles which this user has been assigned."""
        return self.properties.get(
            "appRoleAssignments",
            AppRoleAssignmentCollection(self.context, ResourcePath("appRoleAssignments", self.resource_path)),
        )

    @property
    def chats(self) -> ChatCollection:
        """The user's chats."""
        return self.properties.get(
            "chats",
            ChatCollection(self.context, ResourcePath("chats", self.resource_path)),
        )

    @property
    def display_name(self) -> Optional[str]:
        """The DisplayName property specifies the users's display name."""
        return self.properties.get("displayName", None)

    @property
    def given_name(self) -> Optional[str]:
        """The given name (first name) of the user. Maximum length is 64 characters"""
        return self.properties.get("givenName", None)

    @property
    def my_site(self) -> Optional[str]:
        """The URL for the user's site."""
        return self.properties.get("mySite", None)

    @property
    def office_location(self) -> Optional[str]:
        """The office location in the user's place of business."""
        return self.properties.get("officeLocation", None)

    @property
    def user_principal_name(self) -> Optional[str]:
        """
        The user principal name (UPN) of the user. The UPN is an Internet-style login name for the user based on the
        Internet standard RFC 822. By convention, this should map to the user's email name.
        The general format is alias@domain, where domain must be present in the tenant's collection of verified domains.
        This property is required when a user is created. The verified domains for the tenant can be accessed from
        the verifiedDomains property of organization.
        NOTE: This property cannot contain accent characters.
        Only the following characters are allowed A - Z, a - z, 0 - 9, ' . - _ ! # ^ ~.
        For the complete list of allowed characters, see username policies.
        """
        return self.properties.get("userPrincipalName", None)

    @property
    def assigned_plans(self) -> ClientValueCollection[AssignedPlan]:
        """The plans that are assigned to the user."""
        return self.properties.get("assignedPlans", ClientValueCollection(AssignedPlan))

    @property
    def authentication(self) -> Authentication:
        """
        The authentication methods that are supported for the user.
        """
        return self.properties.get(
            "authentication",
            Authentication(self.context, ResourcePath("authentication", self.resource_path)),
        )

    @property
    def business_phones(self) -> StringCollection:
        """String collection	The telephone numbers for the user. NOTE: Although this is a string collection,
        only one number can be set for this property. Read-only for users synced from on-premises directory.
        """
        return self.properties.get("businessPhones", StringCollection())

    @property
    def creation_type(self) -> Optional[str]:
        """Indicates whether the user account was created as a regular school or work account (null),
        an external account (Invitation), a local account for an Azure Active Directory B2C tenant (LocalAccount)
        or self-service sign-up using email verification (EmailVerified). Read-only.
        """
        return self.properties.get("creationType", None)

    @property
    def license_assignment_states(
        self,
    ) -> ClientValueCollection[LicenseAssignmentState]:
        """
        State of license assignments for this user. Also indicates licenses that are directly-assigned and those
        that the user has inherited through group memberships.
        """
        return self.properties.get("licenseAssignmentStates", ClientValueCollection(LicenseAssignmentState))

    @property
    def mail(self) -> Optional[str]:
        """The SMTP address for the user, for example, "jeff@contoso.onmicrosoft.com".
        Returned by default. Supports $filter and endsWith.
        """
        return self.properties.get("mail", None)

    @property
    def other_mails(self) -> StringCollection:
        """A list of additional email addresses for the user;
        for example: ["bob@contoso.com", "Robert@fabrikam.com"]. Supports $filter.
        """
        return self.properties.get("otherMails", StringCollection())

    @property
    def interests(self) -> StringCollection:
        """A list for the user to describe their interests."""
        return self.properties.get("interests", StringCollection())

    @property
    def identities(self) -> ClientValueCollection[ObjectIdentity]:
        """Represents the identities that can be used to sign in to this user account.
        An identity can be provided by Microsoft (also known as a local account), by organizations,
        or by social identity providers such as Facebook, Google, and Microsoft, and tied to a user account.
        May contain multiple items with the same signInType value.
        Supports $filter.
        """
        return self.properties.get("identities", ClientValueCollection(ObjectIdentity))

    @property
    def activities(self) -> UserActivityCollection:
        """The user's activities across devices."""
        return self.properties.get(
            "activities",
            UserActivityCollection(self.context, ResourcePath("activities", self.resource_path)),
        )

    @property
    def assigned_licenses(self) -> ClientValueCollection[AssignedLicense]:
        """The licenses that are assigned to the user, including inherited (group-based) licenses."""
        return self.properties.get("assignedLicenses", ClientValueCollection(AssignedLicense))

    @property
    def followed_sites(self) -> EntityCollection[Site]:
        """ """
        return self.properties.get(
            "followedSites",
            EntityCollection(self.context, Site, ResourcePath("followedSites", self.resource_path)),
        )

    @property
    def insights(self) -> OfficeGraphInsights:
        """Insights are relationships calculated using advanced analytics and machine learning techniques."""
        return self.properties.get(
            "insights",
            OfficeGraphInsights(self.context, ResourcePath("insights", self.resource_path)),
        )

    @property
    def photo(self):
        """The user's profile photo. Read-only."""
        return self.properties.get(
            "photo",
            ProfilePhoto(self.context, ResourcePath("photo", self.resource_path)),
        )

    @property
    def photos(self):
        """The collection of the user's profile photos in different sizes"""
        return self.properties.get(
            "photos",
            EntityCollection(self.context, ProfilePhoto, ResourcePath("photos", self.resource_path)),
        )

    @property
    def manager(self):
        """The user or contact that is this user's manager"""
        return self.properties.get(
            "manager",
            DirectoryObject(self.context, ResourcePath("manager", self.resource_path)),
        )

    @property
    def preferred_language(self) -> Optional[str]:
        """
        The preferred language for the user. Should follow ISO 639-1 Code; for example en-US.
        """
        return self.properties.get("preferredLanguage", None)

    @property
    def mailbox_settings(self):
        """Get the user's mailboxSettings."""
        return self.properties.get("mailboxSettings", MailboxSettings())

    @mailbox_settings.setter
    def mailbox_settings(self, value):
        self.set_property("mailboxSettings", value)

    @property
    def calendar(self) -> Calendar:
        """The user's primary calendar. Read-only."""
        return self.properties.get(
            "calendar",
            Calendar(self.context, ResourcePath("calendar", self.resource_path)),
        )

    @property
    def calendars(self) -> EntityCollection[Calendar]:
        """The user's calendar groups. Read-only. Nullable."""
        return self.properties.get(
            "calendars",
            EntityCollection(self.context, Calendar, ResourcePath("calendars", self.resource_path)),
        )

    @property
    def calendar_groups(self) -> EntityCollection[CalendarGroup]:
        """The user's calendar groups. Read-only. Nullable."""
        return self.properties.get(
            "calendarGroups",
            EntityCollection(
                self.context,
                CalendarGroup,
                ResourcePath("calendarGroups", self.resource_path),
            ),
        )

    @property
    def license_details(self) -> EntityCollection[LicenseDetails]:
        """Retrieve the properties and relationships of a Drive resource."""
        return self.properties.get(
            "licenseDetails",
            EntityCollection(
                self.context,
                LicenseDetails,
                ResourcePath("licenseDetails", self.resource_path),
            ),
        )

    @property
    def drive(self) -> Drive:
        """Retrieve the properties and relationships of a Drive resource."""
        return self.properties.get(
            "drive",
            Drive(
                self.context,
                EntityPath("drive", self.resource_path, ResourcePath("drives")),
            ),
        )

    @property
    def contacts(self) -> ContactCollection:
        """Get a contact collection from the default Contacts folder of the signed-in user (.../me/contacts),
        or from the specified contact folder."""
        return self.properties.get(
            "contacts",
            ContactCollection(self.context, ResourcePath("contacts", self.resource_path)),
        )

    @property
    def contact_folders(self) -> DeltaCollection[ContactFolder]:
        """Get the contact folder collection in the default Contacts folder of the signed-in user."""
        return self.properties.get(
            "contactFolders",
            DeltaCollection(
                self.context,
                ContactFolder,
                ResourcePath("contactFolders", self.resource_path),
            ),
        )

    @property
    def events(self) -> DeltaCollection[Event]:
        """Get an event collection or an event."""
        return self.properties.get(
            "events",
            DeltaCollection(self.context, Event, ResourcePath("events", self.resource_path)),
        )

    @property
    def messages(self) -> MessageCollection:
        """Get an event collection or an event."""
        return self.properties.get(
            "messages",
            MessageCollection(self.context, ResourcePath("messages", self.resource_path)),
        )

    @property
    def joined_teams(self) -> TeamCollection:
        """Get the teams in Microsoft Teams that the user is a direct member of."""
        return self.properties.get(
            "joinedTeams",
            TeamCollection(self.context, ResourcePath("joinedTeams", self.resource_path)),
        )

    @property
    def managed_devices(self) -> EntityCollection[ManagedDevice]:
        """Devices that are managed or pre-enrolled through Intune"""
        return self.properties.get(
            "managedDevices",
            EntityCollection(
                self.context,
                ManagedDevice,
                ResourcePath("managedDevices", self.resource_path),
            ),
        )

    @property
    def member_of(self) -> DirectoryObjectCollection:
        """Get groups and directory roles that the user is a direct member of."""
        return self.properties.get(
            "memberOf",
            DirectoryObjectCollection(self.context, ResourcePath("memberOf", self.resource_path)),
        )

    @property
    def oauth2_permission_grants(self) -> DeltaCollection[OAuth2PermissionGrant]:
        """"""
        return self.properties.get(
            "oauth2PermissionGrants",
            DeltaCollection(
                self.context,
                OAuth2PermissionGrant,
                ResourcePath("oauth2PermissionGrants", self.resource_path),
            ),
        )

    @property
    def on_premises_distinguished_name(self) -> Optional[str]:
        """
        Contains the on-premises Active Directory distinguished name or DN. The property is only populated for
        customers who are synchronizing their on-premises directory to Azure Active Directory via Azure AD Connect
        """
        return self.properties.get("onPremisesDistinguishedName", None)

    @property
    def on_premises_domain_name(self) -> Optional[str]:
        """
        Contains the on-premises domainFQDN, also called dnsDomainName synchronized from the on-premises directory.
        The property is only populated for customers who are synchronizing their on-premises directory to
        Azure Active Directory via Azure AD Connect.
        """
        return self.properties.get("onPremisesDomainName", None)

    @property
    def owned_devices(self) -> DirectoryObjectCollection:
        """Devices that are owned by the user. Read-only. Nullable.
        Supports $expand and $filter (/$count eq 0, /$count ne 0, /$count eq 1, /$count ne 1).
        """
        return self.properties.get(
            "ownedDevices",
            DirectoryObjectCollection(self.context, ResourcePath("ownedDevices", self.resource_path)),
        )

    @property
    def owned_objects(self) -> DirectoryObjectCollection:
        """Directory objects that are owned by the user. Read-only. Nullable. Supports $expand."""
        return self.properties.get(
            "ownedObjects",
            DirectoryObjectCollection(self.context, ResourcePath("ownedObjects", self.resource_path)),
        )

    @property
    def proxy_addresses(self) -> StringCollection:
        """
        For example: ["SMTP: bob@contoso.com", "smtp: bob@sales.contoso.com"]. Changes to the mail property will
        also update this collection to include the value as an SMTP address. For more information, see mail and
        proxyAddresses properties. The proxy address prefixed with SMTP (capitalized) is the primary proxy address
        while those prefixed with smtp are the secondary proxy addresses. For Azure AD B2C accounts, this
        property has a limit of ten unique addresses. Read-only in Microsoft Graph; you can update this property
        only through the Microsoft 365 admin center. Not nullable.
        """
        return self.properties.get("proxyAddresses", StringCollection())

    @property
    def transitive_member_of(self) -> DirectoryObjectCollection:
        """Get groups, directory roles that the user is a member of. This API request is transitive, and will also
        return all groups the user is a nested member of."""
        return self.properties.get(
            "transitiveMemberOf",
            DirectoryObjectCollection(self.context, ResourcePath("transitiveMemberOf", self.resource_path)),
        )

    @property
    def mail_folders(self) -> MailFolderCollection:
        """Get the mail folder collection under the root folder of the signed-in user."""
        return self.properties.get(
            "mailFolders",
            MailFolderCollection(self.context, ResourcePath("mailFolders", self.resource_path)),
        )

    @property
    def outlook(self) -> OutlookUser:
        """Represents the Outlook services available to a user."""
        return self.properties.get(
            "outlook",
            OutlookUser(self.context, ResourcePath("outlook", self.resource_path)),
        )

    @property
    def people(self) -> EntityCollection[Person]:
        """People that are relevant to the user. Read-only. Nullable."""
        return self.properties.get(
            "people",
            EntityCollection(self.context, Person, ResourcePath("people", self.resource_path)),
        )

    @property
    def onenote(self) -> Onenote:
        """Represents the Onenote services available to a user."""
        return self.properties.get(
            "onenote",
            Onenote(self.context, ResourcePath("onenote", self.resource_path)),
        )

    @property
    def settings(self) -> UserSettings:
        """Represents the user and organization settings object."""
        return self.properties.get(
            "settings",
            UserSettings(self.context, ResourcePath("settings", self.resource_path)),
        )

    @property
    def planner(self) -> PlannerUser:
        """The plannerUser resource provide access to Planner resources for a user."""
        return self.properties.get(
            "planner",
            PlannerUser(self.context, ResourcePath("planner", self.resource_path)),
        )

    @property
    def agreement_acceptances(self) -> EntityCollection[AgreementAcceptance]:
        """
        The user's terms of use acceptance statuses
        """
        return self.properties.get(
            "agreementAcceptances",
            EntityCollection(
                self.context,
                AgreementAcceptance,
                ResourcePath("agreementAcceptances", self.resource_path),
            ),
        )

    @property
    def extensions(self) -> EntityCollection[Extension]:
        """The collection of open extensions defined for the user. Nullable."""
        return self.properties.get(
            "extensions",
            EntityCollection(self.context, Extension, ResourcePath("extensions", self.resource_path)),
        )

    @property
    def direct_reports(self) -> DirectoryObjectCollection:
        """Get a user's direct reports"""
        return self.properties.get(
            "directReports",
            DirectoryObjectCollection(self.context, ResourcePath("directReports", self.resource_path)),
        )

    @property
    def online_meetings(self) -> OnlineMeetingCollection:
        """Get a user's online meetings."""
        return self.properties.get(
            "onlineMeetings",
            OnlineMeetingCollection(self.context, ResourcePath("onlineMeetings", self.resource_path)),
        )

    @property
    def password_policies(self) -> Optional[str]:
        """
        Specifies password policies for the user. This value is an enumeration with one possible value being
        DisableStrongPassword, which allows weaker passwords than the default policy to be specified.
        DisablePasswordExpiration can also be specified. The two may be specified together; for example:
        DisablePasswordExpiration, DisableStrongPassword.
        """
        return self.properties.get("passwordPolicies", None)

    @property
    @persist_property("passwordProfile")
    def password_profile(self) -> PasswordProfile:
        """
        Specifies the password profile for the user. The profile contains the user's password.
        This property is required when a user is created. The password in the profile must satisfy minimum
        requirements as specified by the passwordPolicies property. By default, a strong password is required.
        """
        return self.properties.setdefault("passwordProfile", PasswordProfile())

    @property
    def presence(self) -> Presence:
        """Get a user's presence information."""
        return self.properties.get(
            "presence",
            Presence(self.context, ResourcePath("presence", self.resource_path)),
        )

    @property
    def registered_devices(self) -> DirectoryObjectCollection:
        """Get the devices that are registered for the user from the registeredDevices navigation property."""
        return self.properties.get(
            "registeredDevices",
            DirectoryObjectCollection(self.context, ResourcePath("registeredDevices", self.resource_path)),
        )

    @property
    def street_address(self) -> Optional[str]:
        """The street address of the user's place of business. Maximum length is 1024 characters."""
        return self.properties.get("streetAddress", None)

    @property
    def security_identifier(self) -> Optional[str]:
        """Security identifier (SID) of the user, used in Windows scenarios."""
        return self.properties.get("securityIdentifier", None)

    @property
    def teamwork(self) -> UserTeamwork:
        """A container for the range of Microsoft Teams functionalities that are available per user in the tenant."""
        return self.properties.get(
            "teamwork",
            UserTeamwork(self.context, ResourcePath("teamwork", self.resource_path)),
        )

    @property
    def solutions(self) -> UserSolutionRoot:
        """The identifier that relates the user to the working time schedule triggers. Read-Only. Nullable."""
        return self.properties.get(
            "solutions",
            UserSolutionRoot(self.context, ResourcePath("solutions", self.resource_path)),
        )

    @property
    def todo(self) -> Todo:
        """Represents the To Do services available to a user."""
        return self.properties.get("todo", Todo(self.context, ResourcePath("todo", self.resource_path)))

    @property
    def employee_experience(self) -> EmployeeExperienceUser:
        """Represents the To Do services available to a user."""
        return self.properties.get(
            "employeeExperience",
            EmployeeExperienceUser(self.context, ResourcePath("employeeExperience", self.resource_path)),
        )

    @property
    def usage_location(self) -> Optional[str]:
        """
        A two letter country code (ISO standard 3166). Required for users that will be assigned licenses due to
        legal requirement to check for availability of services in countries. Examples include: US, JP, and GB.
        """
        return self.properties.get("usageLocation", None)

    def get_property(self, name: str, default_value: Any = None):
        if default_value is None:
            property_mapping = {
                "appRoleAssignments": self.app_role_assignments,
                "businessPhones": self.business_phones,
                "calendarGroups": self.calendar_groups,
                "contactFolders": self.contact_folders,
                "createdObjects": self.created_objects,
                "employeeExperience": self.employee_experience,
                "followedSites": self.followed_sites,
                "lastPasswordChangeDateTime": self.last_password_change_datetime,
                "licenseDetails": self.license_details,
                "managedDevices": self.managed_devices,
                "memberOf": self.member_of,
                "transitiveMemberOf": self.transitive_member_of,
                "joinedTeams": self.joined_teams,
                "assignedLicenses": self.assigned_licenses,
                "mailFolders": self.mail_folders,
                "mailboxSettings": self.mailbox_settings,
                "directReports": self.direct_reports,
                "onlineMeetings": self.online_meetings,
                "oauth2PermissionGrants": self.oauth2_permission_grants,
                "ownedDevices": self.owned_devices,
                "ownedObjects": self.owned_objects,
                "passwordProfile": self.password_profile,
                "registeredDevices": self.registered_devices,
                "signInActivity": self.sign_in_activity,
            }
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)

    def set_property(self, name, value, persist_changes=True):
        super().set_property(name, value, persist_changes)
        # fallback: create a new resource path
        if self._resource_path is None:
            if name == "id" or name == "userPrincipalName":
                self._resource_path = ResourcePath(value, self.parent_collection.resource_path)
        return self
