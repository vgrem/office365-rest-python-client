from office365.directory.identitygovernance.accessreview.stage import AccessReviewStage
from office365.entity_collection import EntityCollection


class AccessReviewStageCollection(EntityCollection[AccessReviewStage]):
    """AccessReviewStage collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, AccessReviewStage, resource_path)
