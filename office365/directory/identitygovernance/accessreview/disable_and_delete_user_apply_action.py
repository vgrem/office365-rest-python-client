from __future__ import annotations

from dataclasses import dataclass

from office365.directory.identitygovernance.accessreview.apply_action import AccessReviewApplyAction


@dataclass
class DisableAndDeleteUserApplyAction(AccessReviewApplyAction):
    pass
