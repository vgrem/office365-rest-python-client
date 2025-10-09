from __future__ import annotations

import os
from datetime import datetime
from functools import partial
from os.path import isfile, join
from typing import IO, AnyStr, Callable, Optional, Union

import requests
from typing_extensions import Self

from office365.delta_path import DeltaPath
from office365.entity_collection import EntityCollection
from office365.onedrive.analytics.item_activity_stat import ItemActivityStat
from office365.onedrive.analytics.item_analytics import ItemAnalytics
from office365.onedrive.base_item import BaseItem
from office365.onedrive.driveitems.audio import Audio
from office365.onedrive.driveitems.conflict_behavior import ConflictBehavior
from office365.onedrive.driveitems.geo_coordinates import GeoCoordinates
from office365.onedrive.driveitems.image import Image
from office365.onedrive.driveitems.item_preview_info import ItemPreviewInfo
from office365.onedrive.driveitems.photo import Photo
from office365.onedrive.driveitems.publication_facet import PublicationFacet
from office365.onedrive.driveitems.remote_item import RemoteItem
from office365.onedrive.driveitems.retention_label import ItemRetentionLabel
from office365.onedrive.driveitems.special_folder import SpecialFolder
from office365.onedrive.driveitems.thumbnail_set import ThumbnailSet
from office365.onedrive.driveitems.uploadable_properties import (
    DriveItemUploadableProperties,
)
from office365.onedrive.drives.recipient import DriveRecipient
from office365.onedrive.files.file import File
from office365.onedrive.files.system_info import FileSystemInfo
from office365.onedrive.folders.folder import Folder
from office365.onedrive.internal.paths.children import ChildrenPath
from office365.onedrive.internal.paths.url import UrlPath
from office365.onedrive.listitems.item_reference import ItemReference
from office365.onedrive.listitems.list_item import ListItem
from office365.onedrive.operations.pending import PendingOperations
from office365.onedrive.permissions.collection import PermissionCollection
from office365.onedrive.permissions.permission import Permission
from office365.onedrive.sensitivitylabels.assignment_method import (
    SensitivityLabelAssignmentMethod,
)
from office365.onedrive.sensitivitylabels.extract_result import (
    ExtractSensitivityLabelsResult,
)
from office365.onedrive.shares.shared import Shared
from office365.onedrive.versions.drive_item import DriveItemVersion
from office365.onedrive.workbooks.workbook import Workbook
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.v4.upload_session import UploadSession
from office365.runtime.odata.v4.upload_session_request import UploadSessionRequest
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.queries.upload_session import UploadSessionQuery
from office365.subscriptions.collection import SubscriptionCollection


class DriveItem(BaseItem):
    """The driveItem resource represents a file, folder, or other item stored in a drive. All file system objects in
    OneDrive and SharePoint are returned as driveItem resources"""

    def assign_sensitivity_label(
        self,
        sensitivity_label_id: str,
        assignment_method: SensitivityLabelAssignmentMethod = None,
        justification_text: str = None,
    ):
        """Asynchronously assign a sensitivity label to a driveItem.


        :param justification_text: Justification text for audit purposes, and is required when downgrading/removing
        a label.
        :param sensitivity_label_id: Required. ID of the sensitivity label to be assigned, or empty string to remove
        the sensitivity label.
        :param assignment_method:  The assignment method of the label on the document. Indicates whether
        the assignment of the label was done automatically, standard, or as a privileged operation
        (the equivalent of an administrator operation).

        """
        payload = {
            "sensitivityLabelId": sensitivity_label_id,
            "assignmentMethod": assignment_method,
            "justificationText": justification_text,
        }
        qry = ServiceOperationQuery(self, "assignSensitivityLabel", None, payload, None)
        self.context.add_query(qry)
        return self

    def set_retention_label(self, name: str):
        """Apply (set) a retention label on a driveItem (files and folders). Retention labels
        don't need to be published in a retention label policy to be applied using this method.
        """
        self.retention_label.name = name
        self.retention_label.update()
        return self

    def get_files(
        self, recursive: bool = False, page_size: Optional[int] = None
    ) -> EntityCollection[DriveItem]:
        """Retrieves files
        :param bool recursive: Determines whether to enumerate folders recursively
        :param int page_size: Page size
        """
        return_type = EntityCollection(self.context, DriveItem, self.resource_path)

        def _get_files(parent_drive_item: DriveItem) -> None:
            def _after_loaded(col: EntityCollection[DriveItem]) -> None:
                if col.has_next:
                    return

                for drive_item in col:
                    if drive_item.is_folder:
                        if recursive and drive_item.folder.childCount > 0:
                            _get_files(drive_item)
                    else:
                        return_type.add_child(drive_item)

            parent_drive_item.children.get_all(
                page_size=page_size, page_loaded=_after_loaded
            )

        _get_files(self)
        return return_type

    def get_folders(
        self, recursive: bool = False, page_size: Optional[int] = None
    ) -> EntityCollection[DriveItem]:
        """Retrieves folders
        :param bool recursive: Determines whether to enumerate folders recursively
        :param int page_size: Page size
        """
        return_type = EntityCollection(self.context, DriveItem, self.resource_path)

        def _get_folders(parent: DriveItem) -> None:

            def _after_loaded(col: EntityCollection[DriveItem]) -> None:
                if col.has_next:
                    return

                for drive_item in col:
                    if recursive and drive_item.folder.childCount > 0:
                        _get_folders(drive_item)
                    return_type.add_child(drive_item)

            parent.children.filter("folder ne null").get_all(
                page_size=page_size, page_loaded=_after_loaded
            )

        _get_folders(self)
        return return_type

    def get_by_path(self, url_path: str) -> DriveItem:
        """Retrieve DriveItem by server relative path"""
        return DriveItem(
            self.context, UrlPath(url_path, self.resource_path), self.children
        )

    def create_powerpoint(self, name: str) -> DriveItem:
        """
        Creates a PowerPoint file
        :param str name: File name
        """
        return self.upload(name, None)

    def create_link(
        self,
        link_type: str,
        scope: Optional[str] = None,
        expiration_datetime: Optional[datetime] = None,
        password: Optional[str] = None,
        message: Optional[str] = None,
        retain_inherited_permissions: Optional[bool] = None,
    ) -> Permission:
        """
        The createLink action will create a new sharing link if the specified link type doesn't already exist
        for the calling application. If a sharing link of the specified type already exists for the app,
        the existing sharing link will be returned.

        :param str link_type: The type of sharing link to create. Either view, edit, or embed.
        :param str scope:  The scope of link to create. Either anonymous or organization.
        :param str or datetime.datetime expiration_datetime: A String with format of yyyy-MM-ddTHH:mm:ssZ of DateTime
            indicate the expiration time of the permission.
        :param str password: The password of the sharing link that is set by the creator. Optional
            and OneDrive Personal only.
        :param str message:
        :param bool retain_inherited_permissions: Optional. If true (default), any existing inherited permissions
            are retained on the shared item when sharing this item for the first time.
            If false, all existing permissions are removed when sharing for the first time.
        """
        payload = {
            "type": link_type,
            "scope": scope or "",
            "message": message,
            "expirationDateTime": expiration_datetime,
            "password": password,
            "retainInheritedPermissions": retain_inherited_permissions,
        }
        return_type = Permission(self.context)
        self.permissions.add_child(return_type)
        qry = ServiceOperationQuery(
            self, "createLink", None, payload, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def discard_checkout(self) -> Self:
        """Discard the check out of a driveItem. This action releases a driveItem resource that was previously
        checked out. Any changes made to the item while it was checked out are discarded.

        The same user that performed the checkout must discard it. Another alternative is to use application permissions
        """
        qry = ServiceOperationQuery(self, "discardCheckout")
        self.context.add_query(qry)
        return self

    def extract_sensitivity_labels(
        self,
    ) -> ClientResult[ExtractSensitivityLabelsResult]:
        """
        Extract one or more sensitivity labels assigned to a drive item and update the metadata of a drive
        item with the latest details of the assigned label. In case of failure to extract the sensitivity labels
        of a file, an extraction error will be thrown with the applicable error code and message.
        """
        return_type = ClientResult(self.context, ExtractSensitivityLabelsResult())
        qry = ServiceOperationQuery(
            self, "extractSensitivityLabels", return_type=return_type
        )
        self.context.add_query(qry)
        return return_type

    def follow(self) -> Self:
        """Follow a driveItem."""
        qry = ServiceOperationQuery(self, "follow")
        self.context.add_query(qry)
        return self

    def unfollow(self) -> Self:
        """Unfollow a driveItem."""
        qry = ServiceOperationQuery(self, "unfollow")
        self.context.add_query(qry)
        return self

    def checkout(self) -> Self:
        """
        Check out a driveItem resource to prevent others from editing the document, and prevent your changes
        from being visible until the documented is checked in.
        """
        qry = ServiceOperationQuery(self, "checkout")
        self.context.add_query(qry)
        return self

    def checkin(self, comment: str, checkin_as: Optional[str] = None) -> Self:
        """
        Check in a checked out driveItem resource, which makes the version of the document available to others.

        :param str comment: comment to the new version of the file
        :param str checkin_as: The status of the document after the check-in operation is complete.
            Can be published or unspecified.
        """
        qry = ServiceOperationQuery(
            self, "checkin", None, {"comment": comment, "checkInAs": checkin_as or ""}
        )
        self.context.add_query(qry)
        return self

    def resumable_upload(
        self,
        source_path: str,
        chunk_size: int = 2000000,
        chunk_uploaded: Optional[Callable[[int], None]] = None,
    ) -> DriveItem:
        """
        Create an upload session to allow your app to upload files up to the maximum file size.
        An upload session allows your app to upload ranges of the file in sequential API requests,
        which allows the transfer to be resumed if a connection is dropped while the upload is in progress.

        To upload a file using an upload session, there are two steps:
            Create an upload session
            Upload bytes to the upload session

        :param chunk_uploaded:
        :param str source_path: File path
        :param int chunk_size: chunk size
        """

        def _start_upload(result: ClientResult[UploadSession]) -> None:
            with open(source_path, "rb") as local_file:
                session_request = UploadSessionRequest(
                    local_file, chunk_size, chunk_uploaded
                )
                session_request.execute_query(qry)

        file_name = os.path.basename(source_path)
        return_type = DriveItem(self.context, UrlPath(file_name, self.resource_path))

        qry = UploadSessionQuery(
            return_type, {"item": DriveItemUploadableProperties(name=file_name)}
        )
        self.context.add_query(qry).after_query_execute(_start_upload)
        return return_type

    def create_upload_session(
        self, item: DriveItemUploadableProperties
    ) -> ClientResult[UploadSession]:
        """Creates a temporary storage location where the bytes of the file will be saved until the complete file is
        uploaded.
        """
        qry = UploadSessionQuery(self, {"item": item})
        self.context.add_query(qry)
        return qry.return_type

    def upload(self, name: str, content: Optional[bytes]):
        """The simple upload API allows you to provide the contents of a new file or update the contents of an
        existing file in a single API call.

        Note: This method only supports files up to 4MB in size.

        :param name: The contents of the request body should be the binary stream of the file to be uploaded.
        :type name: str
        :param content: The contents of the request body should be the binary stream of the file to be uploaded.
        :type content: str or bytes or None
        """
        return_type = DriveItem(self.context, UrlPath(name, self.resource_path))
        self.children.add_child(return_type)
        qry = ServiceOperationQuery(
            return_type, "content", None, content, None, return_type
        )

        def _modify_query(request: RequestOptions) -> None:
            request.method = HttpMethod.Put

        self.context.add_query(qry).before_query_execute(_modify_query)
        return return_type

    def upload_file(self, path_or_file: str | IO) -> "DriveItem":
        """Uploads a file"""
        if hasattr(path_or_file, "read"):
            content = path_or_file.read()
            name = os.path.basename(path_or_file.name)
            return self.upload(name, content)
        else:
            with open(path_or_file, "rb") as f:
                content = f.read()
            name = os.path.basename(path_or_file)
            return self.upload(name, content)

    def upload_folder(
        self, path: str, file_uploaded: Callable[["DriveItem"], None] = None
    ) -> DriveItem:

        def _after_file_upload(return_type: DriveItem) -> None:
            if callable(file_uploaded):
                file_uploaded(return_type)

        def _upload_folder(source_path: str, target_folder: "DriveItem") -> None:
            for name in os.listdir(source_path):
                cur_path = join(source_path, name)
                if isfile(cur_path):
                    with open(cur_path, "rb") as f:
                        target_folder.upload_file(f).after_execute(_after_file_upload)
                else:
                    target_folder.create_folder(name).after_execute(
                        partial(_upload_folder, cur_path)
                    )

        """Uploads a folder"""
        _upload_folder(path, self)
        return self

    def get_content(self, format_name: Optional[str] = None) -> ClientResult[AnyStr]:
        """
        Download the contents of the primary stream (file) of a DriveItem.
        Only driveItems with the file property can be downloaded.

        :type format_name: str or None
        """
        return_type = ClientResult(self.context)
        action_name = "content"
        if format_name is not None:
            action_name = action_name + rf"?format={format_name}"
        qry = FunctionQuery(self, action_name, None, return_type)
        self.context.add_query(qry)
        return return_type

    def download(self, file_object: IO) -> Self:
        """
        Download the contents of the primary stream (file) of a DriveItem. Only driveItems with the file property
        can be downloaded
        """

        def _save_content(return_type: ClientResult[AnyStr]) -> None:
            file_object.write(return_type.value)

        self.get_content().after_execute(_save_content)
        return self

    def download_folder(
        self,
        download_file: IO,
        after_file_downloaded: Callable[[DriveItem], None] = None,
        recursive: bool = True,
    ) -> DriveItem:
        """
        Download the folder content
        """
        import zipfile

        def _after_file_downloaded(
            drive_item: DriveItem, base_path: str, result: ClientResult[AnyStr]
        ) -> None:
            with zipfile.ZipFile(download_file.name, "a", zipfile.ZIP_DEFLATED) as zf:
                zip_path = (
                    "/".join([base_path, drive_item.name])
                    if base_path is not None
                    else drive_item.name
                )
                zf.writestr(zip_path, result.value)
                if callable(after_file_downloaded):
                    after_file_downloaded(drive_item)

        def _after_folder_downloaded(
            parent_item: "DriveItem", base_path: str = None
        ) -> None:
            for drive_item in parent_item.children:
                if drive_item.is_file:
                    drive_item.get_content().after_execute(
                        partial(_after_file_downloaded, drive_item, base_path)
                    )
                else:
                    if recursive:
                        if base_path is None:
                            next_base_path = str(drive_item.name)
                        else:
                            next_base_path = "/".join([base_path, drive_item.name])
                        _download_folder(drive_item, next_base_path)

        def _download_folder(drive_item: "DriveItem", prev_result: str = None) -> None:
            drive_item.ensure_properties(
                ["children", "name"],
                partial(_after_folder_downloaded, drive_item, prev_result),
            )

        _download_folder(self)
        return self

    def download_session(
        self,
        file_object: IO,
        chunk_downloaded: Callable[[int], None] = None,
        chunk_size: Optional[int] = 1024 * 1024,
    ) -> Self:
        """
        By default, file gets downloaded immediately.
        For a large files reading the whole content of a file at once into memory should be avoided.

        This method allows to stream content into the file

        :type file_object: typing.IO
        :param (int)->None or None chunk_downloaded: A callback
        :param int chunk_size: The number of bytes it should read into memory.
        """

        def _construct_request(request: RequestOptions) -> None:
            request.stream = True

        def _process_response(response: requests.Response) -> None:
            bytes_read = 0
            for chunk in response.iter_content(chunk_size=chunk_size):
                bytes_read += len(chunk)
                if callable(chunk_downloaded):
                    chunk_downloaded(bytes_read)
                file_object.write(chunk)

        self.get_content().before_execute(_construct_request).after_execute(
            _process_response, include_response=True
        )
        return self

    def create_folder(
        self,
        name: str,
        conflict_behavior: Optional[ConflictBehavior] = ConflictBehavior.Rename,
    ) -> DriveItem:
        """Create a new folder or DriveItem in a Drive with a specified parent item or path.

        :param str name: Folder name
        :param str conflict_behavior: query parameter to customize the behavior when a conflict occurs.
        """
        return_type = DriveItem(self.context)
        self.children.add_child(return_type)
        payload = {
            "name": name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": conflict_behavior.value,
        }
        qry = CreateEntityQuery(self.children, payload, return_type)
        self.context.add_query(qry)
        return return_type

    def convert(self, format_name: str) -> ClientResult[AnyStr]:
        """Converts the contents of an item in a specific format

        :param format_name: Specify the format the item's content should be downloaded as.
        :type format_name: str
        """
        return self.get_content(format_name)

    def copy(
        self,
        name: str = None,
        parent: ItemReference | DriveItem = None,
        conflict_behavior: ConflictBehavior = ConflictBehavior.Fail,
    ) -> ClientResult[str]:
        """Asynchronously creates a copy of an driveItem (including any children), under a new parent item or with a
        new name.

        :param str or None name: The new name for the copy. If this isn't provided, the same name will be used as the
             original.
        :param office365.onedrive.listitems.item_reference.ItemReference or DriveItem or None parent:  Reference to the
             parent item the copy will be created in.
        :param str conflict_behavior: query parameter to customize the behavior when a conflict occurs.

        Returns location for details about how to monitor the progress of the copy, upon accepting the request.
        """
        return_type = ClientResult(self.context, str())

        def _copy(parent_reference: ItemReference) -> None:

            def _create_request(request: RequestOptions) -> None:
                request.url += (
                    f"?@microsoft.graph.conflictBehavior={conflict_behavior.value}"
                )

            def _process_response(resp: requests.Response) -> None:
                resp.raise_for_status()
                location = resp.headers.get("Location", None)
                if location is None:
                    return
                return_type.set_property("__value", location)

            payload = {"name": name, "parentReference": parent_reference}
            qry = ServiceOperationQuery(self, "copy", None, payload, None, return_type)
            self.context.add_query(qry).before_query_execute(
                _create_request
            ).after_execute(_process_response)

        if isinstance(parent, DriveItem):

            def _drive_item_loaded():
                parent_reference = ItemReference(
                    drive_id=parent.parent_reference.driveId, id_=parent.id
                )
                _copy(parent_reference)

            parent.ensure_property("parentReference", _drive_item_loaded)
        else:
            _copy(parent)
        return return_type

    def move(
        self,
        name: str = None,
        parent: ItemReference | DriveItem = None,
        conflict_behavior: ConflictBehavior = ConflictBehavior.Fail,
    ) -> DriveItem:
        """To move a DriveItem to a new parent item, your app requests to update the parentReference of the DriveItem
        to move.

        :param str name: The new name for the move. If this isn't provided, the same name will be used as the
             original.
        :param ItemReference or DriveItem or None parent: Reference to the
             parent item the move will be created in.
        :param str conflict_behavior: query parameter to customize the behavior when a conflict occurs.
        """

        return_type = DriveItem(self.context)
        self.children.add_child(return_type)

        def _move(parent_reference: ItemReference) -> None:
            payload = {"name": name, "parentReference": parent_reference}

            def _construct_request(request: RequestOptions) -> None:
                request.method = HttpMethod.Patch
                request.url += "?@microsoft.graph.conflictBehavior={0}".format(
                    conflict_behavior.value
                )

            qry = ServiceOperationQuery(self, "", None, payload, None, return_type)
            self.context.add_query(qry).before_execute(_construct_request)

        if isinstance(parent, DriveItem):

            def _drive_item_loaded():
                _move(ItemReference(id_=parent.id))

            parent.ensure_property("parentReference", _drive_item_loaded)
        else:
            _move(parent)
        return return_type

    def rename(self, new_name: str) -> DriveItem:
        """Rename a DriveItem
        :param str new_name: The new name for the rename.
        """
        return self.move(name=new_name)

    def search(self, query_text: str) -> EntityCollection["DriveItem"]:
        """Search the hierarchy of items for items matching a query. You can search within a folder hierarchy,
        a whole drive, or files shared with the current user.

        :type query_text: str
        """
        return_type = EntityCollection[DriveItem](
            self.context, DriveItem, ResourcePath("items", self.resource_path)
        )
        qry = FunctionQuery(self, "search", {"q": query_text}, return_type)
        self.context.add_query(qry)
        return return_type

    def invite(
        self,
        recipients: list[str],
        message: str,
        require_sign_in: Optional[bool] = True,
        send_invitation: Optional[bool] = True,
        roles: Optional[list[str]] = None,
        expiration_datetime: Optional[datetime] = None,
        password: Optional[str] = None,
        retain_inherited_permissions: Optional[bool] = None,
    ) -> PermissionCollection:
        """
        Sends a sharing invitation for a driveItem. A sharing invitation provides permissions to the recipients
        and optionally sends them an email with a sharing link.

        :param list[str] recipients: A collection of recipients who will receive access and the sharing
            invitation.
        :param str message: A plain text formatted message that is included in the sharing invitation.
            Maximum length 2000 characters.
        :param bool require_sign_in: Specifies whether the recipient of the invitation is required to sign-in to view
            the shared item.
        :param bool send_invitation: If true, a sharing link is sent to the recipient. Otherwise, a permission is
            granted directly without sending a notification.
        :param list[str] roles: Specify the roles that are to be granted to the recipients of the sharing invitation.
        :param datetime.datetime expiration_datetime: Specifies the dateTime after which the permission expires.
            For OneDrive for Business and SharePoint, expirationDateTime is only applicable for sharingLink permissions.
            Available on OneDrive for Business, SharePoint, and premium personal OneDrive accounts.
        :param str password: The password set on the invite by the creator. Optional and OneDrive Personal only.
        :param bool retain_inherited_permissions: Optional. If true (default), any existing inherited permissions
            are retained on the shared item when sharing this item for the first time. If false, all existing
            permissions are removed when sharing for the first time.
        """
        if roles is None:
            roles = ["read"]
        return_type = PermissionCollection(self.context)
        payload = {
            "requireSignIn": require_sign_in,
            "sendInvitation": send_invitation,
            "roles": roles,
            "recipients": ClientValueCollection(
                DriveRecipient, [DriveRecipient.from_email(r) for r in recipients]
            ),
            "message": message,
            "expirationDateTime": (
                expiration_datetime.isoformat() + "Z" if expiration_datetime else None
            ),
            "password": password,
            "retainInheritedPermissions": retain_inherited_permissions,
        }
        qry = ServiceOperationQuery(self, "invite", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_activities_by_interval(self, start_dt=None, end_dt=None, interval=None):
        """
        Get a collection of itemActivityStats resources for the activities that took place on this resource
        within the specified time interval.

        :param datetime.datetime start_dt: The start time over which to aggregate activities.
        :param datetime.datetime end_dt: The end time over which to aggregate activities.
        :param str interval: The aggregation interval.
        """
        return_type = EntityCollection(
            self.context, ItemActivityStat, self.resource_path
        )

        params = {
            "startDateTime": start_dt.strftime("%m-%d-%Y") if start_dt else None,
            "endDateTime": end_dt.strftime("%m-%d-%Y") if end_dt else None,
            "interval": interval,
        }

        qry = FunctionQuery(self, "getActivitiesByInterval", params, return_type)
        self.context.add_query(qry)
        return return_type

    def permanent_delete(self):
        """
        Permanently delete a driveItem.
        Note that if you delete items using this method, they will be permanently removed and won't be sent to the
        recycle bin. Therefore, they cannot be restored afterward. For non-permanent delete, use delete_object()
        """
        qry = ServiceOperationQuery(self, "permanentDelete")
        self.context.add_query(qry)
        return self

    def restore(
        self, parent_reference: Optional[ItemReference] = None, name: str = None
    ) -> DriveItem:
        """
        Restore a driveItem that has been deleted and is currently in the recycle bin.
        NOTE: This functionality is currently only available for OneDrive Personal.

        :param str name: Optional. The new name for the restored item. If this isn't provided,
             the same name will be used as the original.
        :param ItemReference or None parent_reference: Optional. Reference to the parent item the deleted item will
             be restored to.
        """
        payload = {"name": name, "parentReference": parent_reference}
        return_type = DriveItem(self.context)
        self.children.add_child(return_type)
        qry = ServiceOperationQuery(self, "restore", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def preview(
        self, page: Union[str, int], zoom: Optional[int] = None
    ) -> ClientResult[ItemPreviewInfo]:
        """
        This action allows you to obtain a short-lived embeddable URL for an item in order
        to render a temporary preview.

        :param str or int page: Optional. Page number of document to start at, if applicable.
            Specified as string for future use cases around file types such as ZIP.
        :param int zoom: Optional. Zoom level to start at, if applicable.

        """
        payload = {"page": page, "zoom": zoom}
        return_type = ClientResult(self.context, ItemPreviewInfo())
        qry = ServiceOperationQuery(self, "preview", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def validate_permission(
        self, challenge_token: Optional[str] = None, password: Optional[str] = None
    ) -> Self:
        """ """
        payload = {"challengeToken": challenge_token, "password": password}
        qry = ServiceOperationQuery(self, "validatePermission", None, payload)
        self.context.add_query(qry)
        return self

    @property
    def audio(self) -> Audio:
        """Audio metadata, if the item is an audio file. Read-only."""
        return self.properties.get("audio", Audio())

    @property
    def image(self) -> Image:
        """
        Image metadata, if the item is an image. Read-only.
        """
        return self.properties.get("image", Image())

    @property
    def photo(self) -> Photo:
        """Photo metadata, if the item is a photo. Read-only."""
        return self.properties.get("photo", Photo())

    @property
    def location(self) -> GeoCoordinates:
        """Location metadata, if the item has location data"""
        return self.properties.get("location", GeoCoordinates())

    @property
    def file_system_info(self) -> FileSystemInfo:
        """File system information on client."""
        return self.properties.get("fileSystemInfo", FileSystemInfo())

    @property
    def folder(self) -> Folder:
        """Folder metadata, if the item is a folder."""
        return self.properties.get("folder", Folder())

    @property
    def file(self) -> File:
        """File metadata, if the item is a file."""
        return self.properties.get("file", File())

    @property
    def is_folder(self) -> bool:
        """Determines whether the provided drive item is folder facet"""
        return self.is_property_available("folder")

    @property
    def is_file(self) -> bool:
        """Determines whether the provided drive item is file facet"""
        return self.is_property_available("file")

    @property
    def shared(self) -> Shared:
        """Indicates that the item has been shared with others and provides information about the shared state
        of the item. Read-only."""
        return self.properties.get("shared", Shared())

    @property
    def web_dav_url(self) -> Optional[str]:
        """WebDAV compatible URL for the item."""
        return self.properties.get("webDavUrl", None)

    @property
    def children(self) -> EntityCollection["DriveItem"]:
        """Collection containing Item objects for the immediate children of Item. Only items representing folders
        have children.
        """
        return self.properties.get(
            "children",
            EntityCollection(self.context, DriveItem, ChildrenPath(self.resource_path)),
        )

    @property
    def listItem(self) -> ListItem:
        """For drives in SharePoint, the associated document library list item."""
        return self.properties.get(
            "listItem",
            ListItem(self.context, ResourcePath("listItem", self.resource_path)),
        )

    @property
    def workbook(self) -> Workbook:
        """For files that are Excel spreadsheets, accesses the workbook API to work with the spreadsheet's contents."""
        return self.properties.get(
            "workbook",
            Workbook(self.context, ResourcePath("workbook", self.resource_path)),
        )

    @property
    def pending_operations(self) -> PendingOperations:
        """If present, indicates that one or more operations that might affect the state of the driveItem are pending
        completion. Read-only."""
        return self.properties.get("pendingOperations", PendingOperations())

    @property
    def permissions(self) -> PermissionCollection:
        """The set of permissions for the item. Read-only. Nullable."""
        return self.properties.get(
            "permissions",
            PermissionCollection(
                self.context, ResourcePath("permissions", self.resource_path)
            ),
        )

    @property
    def retention_label(self) -> ItemRetentionLabel:
        """Information about retention label and settings enforced on the driveItem."""
        return self.properties.setdefault(
            "retentionLabel",
            ItemRetentionLabel(
                self.context, ResourcePath("retentionLabel", self.resource_path)
            ),
        )

    @property
    def publication(self) -> PublicationFacet:
        """Provides information about the published or checked-out state of an item,
        in locations that support such actions. This property is not returned by default. Read-only.
        """
        return self.properties.get("publication", PublicationFacet())

    @property
    def remote_item(self) -> RemoteItem:
        """Remote item data, if the item is shared from a drive other than the one being accessed. Read-only."""
        return self.properties.get("remoteItem", RemoteItem())

    @property
    def special_folder(self) -> SpecialFolder:
        """If the current item is also available as a special folder, this facet is returned. Read-only."""
        return self.properties.get("specialFolder", SpecialFolder())

    @property
    def versions(self) -> EntityCollection[DriveItemVersion]:
        """The list of previous versions of the item. For more info, see getting previous versions.
        Read-only. Nullable."""
        return self.properties.get(
            "versions",
            EntityCollection(
                self.context,
                DriveItemVersion,
                ResourcePath("versions", self.resource_path),
            ),
        )

    @property
    def thumbnails(self) -> EntityCollection[ThumbnailSet]:
        """Collection containing ThumbnailSet objects associated with the item. For more info, see getting thumbnails.
        Read-only. Nullable."""
        return self.properties.get(
            "thumbnails",
            EntityCollection(
                self.context,
                ThumbnailSet,
                ResourcePath("thumbnails", self.resource_path),
            ),
        )

    @property
    def analytics(self) -> ItemAnalytics:
        """Analytics about the view activities that took place on this item."""
        return self.properties.get(
            "analytics",
            ItemAnalytics(self.context, ResourcePath("analytics", self.resource_path)),
        )

    @property
    def delta(self) -> EntityCollection[DriveItem]:
        """This method allows your app to track changes to a drive item and its children over time."""
        return self.properties.get(
            "delta",
            EntityCollection(self.context, DriveItem, DeltaPath(self.resource_path)),
        )

    @property
    def subscriptions(self) -> SubscriptionCollection:
        """The set of subscriptions on the driveItem."""
        return self.properties.get(
            "subscriptions",
            SubscriptionCollection(
                self.context, ResourcePath("subscriptions", self.resource_path)
            ),
        )

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "fileSystemInfo": self.file_system_info,
                "remoteItem": self.remote_item,
                "specialFolder": self.special_folder,
            }
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)
