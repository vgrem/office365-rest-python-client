from office365.directory.security.labels.retention.duration import RetentionDuration
from office365.directory.security.labels.retention.label import RetentionLabel
from office365.directory.security.labels.retention.trigger import RetentionTrigger
from office365.directory.security.labels.retention.types import (
    ActionAfterRetentionPeriod,
    BehaviorDuringRetentionPeriod,
    DefaultRecordBehavior,
)
from office365.entity_collection import EntityCollection
from office365.runtime.http.request_options import RequestOptions


class RetentionLabelCollection(EntityCollection[RetentionLabel]):
    """"""

    def __init__(self, context, resource_path=None):
        super(RetentionLabelCollection, self).__init__(
            context, RetentionLabel, resource_path
        )

    def add(
        self,
        display_name: str,
        retention_trigger: RetentionTrigger,
        retention_duration: RetentionDuration,
        behavior_during_retention_period: BehaviorDuringRetentionPeriod,
        default_record_behavior: DefaultRecordBehavior,
        action_after_retention_period: ActionAfterRetentionPeriod,
    ):
        """
        Create a new retentionLabel object.

        To create a disposition review stage, include the actionAfterRetentionPeriod property in the request body
        with one of the possible values specified.
        """

        def _construct_request(request: RequestOptions) -> None:
            request.set_header("Content-Type", "application/json")

        return (
            super()
            .add(
                displayName=display_name,
                retentionTrigger=retention_trigger.name,
                retentionDuration=retention_duration,
                behaviorDuringRetentionPeriod=behavior_during_retention_period.name,
                defaultRecordBehavior=default_record_behavior.name,
                actionAfterRetentionPeriod=action_after_retention_period.name,
            )
            .before_execute(_construct_request)
        )
