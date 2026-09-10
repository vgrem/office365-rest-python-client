from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

import requests
from typing_extensions import Self

from office365.directory.groups.collection import GroupCollection
from office365.entity_collection import EntityCollection
from office365.runtime.paths.builder import ODataPathBuilder
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v4.entity import EntityPath
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.runtime.queries.function import FunctionQuery
from office365.teams.chats.messages.collection import ChatMessageCollection
from office365.teams.operations.async_operation import TeamsAsyncOperation, wait_for_operation
from office365.teams.team import Team

if TYPE_CHECKING:
    from office365.runtime.operations import ProgressCallback


class TeamCollection(EntityCollection[Team]):
    """Team's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, Team, resource_path)

    def get_all(
        self,
        page_size: int | None = None,
        page_loaded: Callable[[Any], None] | None = None,
        progress: "ProgressCallback | None" = None,
    ) -> Self:
        """List all teams in Microsoft Teams for an organization"""

        def _init_teams(groups: GroupCollection) -> None:
            for grp in groups:
                team = Team(self.context, ResourcePath(grp.id, self.resource_path))
                team.copy_from(grp)
                self.add_child(team)
            if callable(page_loaded):
                page_loaded(self)

        self.context.groups.filter("resourceProvisioningOptions/Any(x:x eq 'Team')").get_all(
            page_size, page_loaded=_init_teams, progress=progress
        )
        return self

    def get_all_messages(self) -> ChatMessageCollection:
        """Export every channel message across all teams (``GET /teams/getAllMessages``).

        Application-only (``Teamwork.Migrate.All``). Deferred — run with
        ``execute_query()``.

        Chain ``.filter(...)``/``.select(...)``/``.top(...)`` on the returned
        collection to shape the request.
        """
        return_type = ChatMessageCollection(self.context, self.resource_path)
        qry = FunctionQuery(self, "getAllMessages", None, return_type)
        self.context.add_query(qry)
        return return_type

    def create(
        self,
        display_name: str,
        description: str | None = None,
        template: str = "standard",
    ) -> TeamsAsyncOperation:
        """Create a new team (async) — returns the ``teamsAsyncOperation``.

        The operation is submitted on ``execute_query()`` (HTTP 202). Poll the
        returned operation (:meth:`TeamsAsyncOperation.poll_for_status`) to wait
        for provisioning; ``target_resource_id`` then holds the team id. Use
        :meth:`create_and_wait` for the convenience path that returns a ready
        team.

        Args:
            display_name (str): The name of the team.
            description (str or None): An optional description for the team. Maximum length: 1024 characters.
            template (str): The team template to create from (default ``"standard"``).
        """
        return_type = TeamsAsyncOperation(self.context, EntityPath(None, self.resource_path))

        def _process_response(resp: requests.Response) -> None:
            loc = resp.headers.get("Location")
            if loc is not None:
                operation_path = ODataPathBuilder.parse_url(loc)
                return_type._resource_path = operation_path

        payload = {
            "displayName": display_name,
            "description": description,
            "template@odata.bind": f"{self.context.teams_templates.resource_url}('{template}')",
        }
        qry = CreateEntityQuery(self, payload, return_type)
        self.context.add_query(qry).after_execute(_process_response, include_response=True)
        return return_type

    def create_and_wait(
        self,
        display_name: str,
        description: str | None = None,
        template: str = "standard",
    ) -> Team:
        """Create a team and wait for provisioning (deferred).

        Chains the async creation, the ``teamsAsyncOperation`` poll, and a full
        team ``GET`` through ``after_execute`` hooks — one ``execute_query()``
        returns a provisioned :class:`Team` with its properties loaded.

        Args:
            display_name (str): The name of the team.
            description (str or None): An optional description for the team. Maximum length: 1024 characters.
            template (str): The team template to create from (default ``"standard"``).
        """
        return_type = Team(self.context)
        self.add_child(return_type)

        def _process_response(resp: requests.Response) -> None:
            content_loc = resp.headers.get("Content-Location")
            assert content_loc is not None
            team_path = ODataPathBuilder.parse_url(content_loc)
            return_type.set_property("id", team_path.segment, False)

            loc = resp.headers.get("Location")
            assert loc is not None
            operation = TeamsAsyncOperation(self.context, ODataPathBuilder.parse_url(loc))

            def _on_succeeded(_op) -> None:
                return_type.get()  # queue a full GET to load the team's properties

            wait_for_operation(operation, success_callback=_on_succeeded)

        payload = {
            "displayName": display_name,
            "description": description,
            "template@odata.bind": f"{self.context.teams_templates.resource_url}('{template}')",
        }
        qry = CreateEntityQuery(self, payload, return_type)
        self.context.add_query(qry).after_execute(_process_response, include_response=True)
        return return_type
