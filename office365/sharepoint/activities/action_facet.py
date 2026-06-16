from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.activities.facets.add_to_onedrive import AddToOneDriveFacet
from office365.sharepoint.activities.facets.archive_facet import ArchiveFacet
from office365.sharepoint.activities.facets.checkin import CheckinFacet
from office365.sharepoint.activities.facets.checkout import CheckoutFacet
from office365.sharepoint.activities.facets.create import CreateFacet
from office365.sharepoint.activities.facets.delete import DeleteFacet
from office365.sharepoint.activities.facets.discard_checkout import DiscardCheckoutFacet
from office365.sharepoint.activities.facets.edit import EditFacet
from office365.sharepoint.activities.facets.get_comment import GetCommentFacet
from office365.sharepoint.activities.facets.get_mention import GetMentionFacet
from office365.sharepoint.activities.facets.move import MoveFacet
from office365.sharepoint.activities.facets.point_in_time_restore import PointInTimeRestoreFacet
from office365.sharepoint.activities.facets.reactivate_facet import ReactivateFacet
from office365.sharepoint.activities.facets.rename import RenameFacet
from office365.sharepoint.activities.facets.sharing import SharingFacet
from office365.sharepoint.activities.facets.task_completed import TaskCompletedFacet
from office365.sharepoint.activities.facets.taskcreated import TaskCreatedFacet
from office365.sharepoint.activities.facets.taskreopened import TaskReopenedFacet
from office365.sharepoint.activities.facets.version import VersionFacet
from office365.sharepoint.activities.taskreassignedfacet import TaskReassignedFacet
from office365.sharepoint.sharing.restorefacet import RestoreFacet
from office365.sharepoint.sharing.restoreversionfacet import RestoreVersionFacet


@dataclass
class ActionFacet(ClientValue):
    addToOneDrive: AddToOneDriveFacet = field(default_factory=AddToOneDriveFacet)
    checkin: CheckinFacet = field(default_factory=CheckinFacet)
    checkout: CheckoutFacet = field(default_factory=CheckoutFacet)
    comment: GetCommentFacet = field(default_factory=GetCommentFacet)
    create: CreateFacet = field(default_factory=CreateFacet)
    delete: DeleteFacet = field(default_factory=DeleteFacet)
    discardCheckout: DiscardCheckoutFacet = field(default_factory=DiscardCheckoutFacet)
    edit: EditFacet = field(default_factory=EditFacet)
    mention: GetMentionFacet = field(default_factory=GetMentionFacet)
    move: MoveFacet = field(default_factory=MoveFacet)
    pointInTimeRestore: PointInTimeRestoreFacet = field(default_factory=PointInTimeRestoreFacet)
    rename: RenameFacet = field(default_factory=RenameFacet)
    share: SharingFacet = field(default_factory=SharingFacet)
    taskCompleted: TaskCompletedFacet = field(default_factory=TaskCompletedFacet)
    version: VersionFacet = field(default_factory=VersionFacet)
    restore: RestoreFacet = field(default_factory=RestoreFacet)
    restoreVersion: RestoreVersionFacet = field(default_factory=RestoreVersionFacet)
    taskCreated: TaskCreatedFacet = field(default_factory=TaskCreatedFacet)
    taskReassigned: TaskReassignedFacet = field(default_factory=TaskReassignedFacet)
    taskReopened: TaskReopenedFacet = field(default_factory=TaskReopenedFacet)
    archive: ArchiveFacet = field(default_factory=ArchiveFacet)
    reactivate: ReactivateFacet = field(default_factory=ReactivateFacet)

    def __repr__(self):
        return self.facet_type or ""

    @property
    def facet_type(self):
        return next((n for n, v in self if v), None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActionFacet"
