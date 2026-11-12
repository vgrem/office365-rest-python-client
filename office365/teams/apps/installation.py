from __future__ import annotations

from typing_extensions import Self

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb
from office365.teams.apps.app import TeamsApp
from office365.teams.apps.definition import TeamsAppDefinition
from office365.teams.apps.permission_set import TeamsAppPermissionSet


class TeamsAppInstallation(Entity):
    """
    Represents a teamsApp installed in a team or the personal scope of a user. Any bots that are part of the app will
    become part of any team or user's personal scope that the app is added to.
    """

    @odata(name="teamsApp", navigation=True)
    @property
    def teams_app(self) -> TeamsApp:
        """The app that is installed."""
        return self.properties.get(
            "teamsApp",
            TeamsApp(self.context, ResourcePath("teamsApp", self.resource_path)),
        )

    @odata(name="teamsAppDefinition", navigation=True)
    @property
    def teams_app_definition(self) -> TeamsAppDefinition:
        """The details of this version of the app."""
        return self.properties.get(
            "teamsAppDefinition",
            TeamsAppDefinition(self.context, ResourcePath("teamsAppDefinition", self.resource_path)),
        )

    @odata(name="consentedPermissionSet")
    @property
    def consented_permission_set(self) -> TeamsAppPermissionSet:
        """Gets the consentedPermissionSet property"""
        return self.properties.get("consentedPermissionSet", TeamsAppPermissionSet())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamsAppInstallation"

    @verb(role="action", effect="write")
    @require_permission(
        delegated=[
            "TeamsAppInstallation.ReadWriteSelfForTeam",
            "Directory.ReadWrite.All",
            "Group.ReadWrite.All",
            "TeamsAppInstallation.ManageSelectedForTeam",
            "TeamsAppInstallation.ReadWriteAndConsentForTeam",
            "TeamsAppInstallation.ReadWriteAndConsentSelfForTeam",
            "TeamsAppInstallation.ReadWriteForTeam",
        ],
        application=[
            "TeamsAppInstallation.ReadWriteSelfForTeam.All",
            "Directory.ReadWrite.All",
            "Group.ReadWrite.All",
            "TeamsAppInstallation.ManageSelectedForTeam.All",
            "TeamsAppInstallation.ReadWriteAndConsentForTeam.All",
            "TeamsAppInstallation.ReadWriteAndConsentSelfForTeam.All",
            "TeamsAppInstallation.ReadWriteForTeam.All",
        ],
    )
    def upgrade(self, consented_permission_set: TeamsAppPermissionSet) -> Self:
        """upgrade operation.

        Args:
            consented_permission_set (TeamsAppPermissionSet):
                consentedPermissionSet parameter
        """
        qry = ServiceOperationQuery(
            self, "upgrade", None, {"consentedPermissionSet": consented_permission_set}, None, None
        )
        self.context.add_query(qry)
        return self
