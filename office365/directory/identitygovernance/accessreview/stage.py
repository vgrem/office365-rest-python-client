from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.accessreview.instance_decision_item import (
    AccessReviewInstanceDecisionItem,
)
from office365.directory.identitygovernance.accessreview.reviewer_scope import AccessReviewReviewerScope
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class AccessReviewStage(Entity):
    """
    Represents a stage of a Microsoft Entra access review. If the parent accessReviewScheduleDefinition has defined
    the stageSettings property, the accessReviewInstance is comprised of up to three subsequent stages.
    Each stage may have a different set of reviewers who can act on the stage decisions, and settings determining
    which decisions pass from stage to stage.

    Every accessReviewStage contains a list of decision items for reviewers.
    There's only one decision per identity being reviewed.
    """

    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> datetime:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", datetime.min)

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> datetime:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> Optional[str]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @odata(name="decisions", navigation=True)
    @property
    def decisions(self) -> EntityCollection[AccessReviewInstanceDecisionItem]:
        """Gets the decisions property"""
        return self.properties.get(
            "decisions",
            EntityCollection[AccessReviewInstanceDecisionItem](
                self.context, AccessReviewInstanceDecisionItem, ResourcePath("decisions", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewStage"

    @odata(name="fallbackReviewers")
    @property
    def fallback_reviewers(self) -> ClientValueCollection[AccessReviewReviewerScope]:
        """Gets the fallbackReviewers property"""
        return self.properties.get(
            "fallbackReviewers", ClientValueCollection[AccessReviewReviewerScope](AccessReviewReviewerScope)
        )

    @odata(name="reviewers")
    @property
    def reviewers(self) -> ClientValueCollection[AccessReviewReviewerScope]:
        """Gets the reviewers property"""
        return self.properties.get(
            "reviewers", ClientValueCollection[AccessReviewReviewerScope](AccessReviewReviewerScope)
        )
