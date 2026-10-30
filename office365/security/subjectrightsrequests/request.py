from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.privacy.datasubjecttype import DataSubjectType
from office365.directory.privacy.subjectrightsrequeststatus import SubjectRightsRequestStatus
from office365.directory.privacy.subjectrightsrequesttype import SubjectRightsRequestType
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identity_set import IdentitySet
    from office365.directory.permissions.identity import Identity
    from office365.directory.users.user import User
    from office365.security.subjectrightsrequests.authored_note import (
        AuthoredNote,
    )
    from office365.security.subjectrightsrequests.data_subject import (
        DataSubject,
    )
    from office365.security.subjectrightsrequests.detail import (
        SubjectRightsRequestDetail,
    )
    from office365.security.subjectrightsrequests.history import (
        SubjectRightsRequestHistory,
    )
    from office365.security.subjectrightsrequests.mailbox_location import (
        SubjectRightsRequestMailboxLocation,
    )
    from office365.security.subjectrightsrequests.site_location import (
        SubjectRightsRequestSiteLocation,
    )
    from office365.security.subjectrightsrequests.stage_detail import (
        SubjectRightsRequestStageDetail,
    )
    from office365.teams.team import Team


class SubjectRightsRequest(Entity):
    """Represents the properties of a subject rights request, which is a formal request by a data subject to
    a controller to take an action on their personal data."""

    @odata(name="assignedTo")
    @property
    def assigned_to(self) -> Identity:
        """Gets the assignedTo property"""
        from office365.directory.permissions.identity import Identity

        return self.properties.get("assignedTo", Identity())

    @odata(name="closedDateTime")
    @property
    def closed_date_time(self) -> Optional[datetime]:
        """Gets the closedDateTime property"""
        return self.properties.get("closedDateTime", datetime.min)

    @odata(name="contentQuery")
    @property
    def content_query(self) -> Optional[str]:
        """Gets the contentQuery property"""
        return self.properties.get("contentQuery", None)

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """Gets the createdBy property"""
        from office365.directory.identity_set import IdentitySet

        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="dataSubject")
    @property
    def data_subject(self) -> DataSubject:
        """Gets the dataSubject property"""
        from office365.security.subjectrightsrequests.data_subject import (
            DataSubject,
        )

        return self.properties.get("dataSubject", DataSubject())

    @odata(name="dataSubjectType")
    @property
    def data_subject_type(self) -> DataSubjectType:
        """Gets the dataSubjectType property"""
        return self.properties.get("dataSubjectType", DataSubjectType.customer)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="externalId")
    @property
    def external_id(self) -> Optional[str]:
        """Gets the externalId property"""
        return self.properties.get("externalId", None)

    @odata(name="history")
    @property
    def history(self) -> ClientValueCollection[SubjectRightsRequestHistory]:
        """Gets the history property"""
        from office365.security.subjectrightsrequests.history import (
            SubjectRightsRequestHistory,
        )

        return self.properties.get(
            "history", ClientValueCollection[SubjectRightsRequestHistory](SubjectRightsRequestHistory)
        )

    @odata(name="includeAllVersions")
    @property
    def include_all_versions(self) -> Optional[bool]:
        """Gets the includeAllVersions property"""
        return self.properties.get("includeAllVersions", None)

    @odata(name="includeAuthoredContent")
    @property
    def include_authored_content(self) -> Optional[bool]:
        """Gets the includeAuthoredContent property"""
        return self.properties.get("includeAuthoredContent", None)

    @odata(name="insight")
    @property
    def insight(self) -> SubjectRightsRequestDetail:
        """Gets the insight property"""
        from office365.security.subjectrightsrequests.detail import (
            SubjectRightsRequestDetail,
        )

        return self.properties.get("insight", SubjectRightsRequestDetail())

    @odata(name="internalDueDateTime")
    @property
    def internal_due_date_time(self) -> Optional[datetime]:
        """Gets the internalDueDateTime property"""
        return self.properties.get("internalDueDateTime", datetime.min)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> IdentitySet:
        """Gets the lastModifiedBy property"""
        from office365.directory.identity_set import IdentitySet

        return self.properties.get("lastModifiedBy", IdentitySet())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="mailboxLocations")
    @property
    def mailbox_locations(self) -> SubjectRightsRequestMailboxLocation:
        """Gets the mailboxLocations property"""
        from office365.security.subjectrightsrequests.mailbox_location import (
            SubjectRightsRequestMailboxLocation,
        )

        return self.properties.get("mailboxLocations", SubjectRightsRequestMailboxLocation())

    @odata(name="pauseAfterEstimate")
    @property
    def pause_after_estimate(self) -> Optional[bool]:
        """Gets the pauseAfterEstimate property"""
        return self.properties.get("pauseAfterEstimate", None)

    @odata(name="regulations")
    @property
    def regulations(self) -> StringCollection:
        """Gets the regulations property"""
        return self.properties.get("regulations", StringCollection())

    @odata(name="siteLocations")
    @property
    def site_locations(self) -> SubjectRightsRequestSiteLocation:
        """Gets the siteLocations property"""
        from office365.security.subjectrightsrequests.site_location import (
            SubjectRightsRequestSiteLocation,
        )

        return self.properties.get("siteLocations", SubjectRightsRequestSiteLocation())

    @odata(name="stages")
    @property
    def stages(self) -> ClientValueCollection[SubjectRightsRequestStageDetail]:
        """Gets the stages property"""
        from office365.security.subjectrightsrequests.stage_detail import (
            SubjectRightsRequestStageDetail,
        )

        return self.properties.get(
            "stages", ClientValueCollection[SubjectRightsRequestStageDetail](SubjectRightsRequestStageDetail)
        )

    @odata(name="status")
    @property
    def status(self) -> SubjectRightsRequestStatus:
        """Gets the status property"""
        return self.properties.get("status", SubjectRightsRequestStatus.active)

    @odata(name="type")
    @property
    def type(self) -> SubjectRightsRequestType:
        """Gets the type property"""
        return self.properties.get("type", SubjectRightsRequestType.export)

    @odata(name="approvers", navigation=True)
    @property
    def approvers(self) -> EntityCollection[User]:
        """Gets the approvers property"""
        from office365.directory.users.user import User

        return self.properties.get(
            "approvers", EntityCollection[User](self.context, User, ResourcePath("approvers", self.resource_path))
        )

    @odata(name="collaborators", navigation=True)
    @property
    def collaborators(self) -> EntityCollection[User]:
        """Gets the collaborators property"""
        from office365.directory.users.user import User

        return self.properties.get(
            "collaborators",
            EntityCollection[User](self.context, User, ResourcePath("collaborators", self.resource_path)),
        )

    @odata(name="notes", navigation=True)
    @property
    def notes(self) -> EntityCollection[AuthoredNote]:
        """Gets the notes property"""
        from office365.security.subjectrightsrequests.authored_note import (
            AuthoredNote,
        )

        return self.properties.get(
            "notes",
            EntityCollection[AuthoredNote](self.context, AuthoredNote, ResourcePath("notes", self.resource_path)),
        )

    @odata(name="team", navigation=True)
    @property
    def team(self) -> Team:
        """Gets the team property"""
        from office365.teams.team import Team

        return self.properties.get("team", Team(self.context, ResourcePath("team", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SubjectRightsRequest"
