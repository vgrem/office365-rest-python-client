from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.directory.permissions.identity_set import IdentitySet
from office365.onedrive.driveitems.image import Image
from office365.onedrive.driveitems.package import Package
from office365.onedrive.driveitems.special_folder import SpecialFolder
from office365.onedrive.driveitems.video import Video
from office365.onedrive.files.file import File
from office365.onedrive.files.system_info import FileSystemInfo
from office365.onedrive.folders.folder import Folder
from office365.onedrive.listitems.item_reference import ItemReference
from office365.onedrive.shares.shared import Shared
from office365.runtime.client_value import ClientValue


@dataclass
class RemoteItem(ClientValue):
    """
    The remoteItem resource indicates that a driveItem references an item that exists in another drive.
    This resource provides the unique IDs of the source drive and target item.

    DriveItems with a non-null remoteItem facet are resources that are shared, added to the user's OneDrive,
    or on items returned from heterogeneous collections of items (like search results).
    """

    id: str | None = None
    createdBy: IdentitySet | None = field(default_factory=IdentitySet)
    createdDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    file: File | None = field(default_factory=File)
    fileSystemInfo: FileSystemInfo | None = field(default_factory=FileSystemInfo)
    folder: Folder | None = field(default_factory=Folder)
    image: Image | None = field(default_factory=Image)
    shared: Shared | None = field(default_factory=Shared)
    lastModifiedBy: IdentitySet = field(default_factory=IdentitySet)
    lastModifiedDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    name: str | None = None
    package: Package = field(default_factory=Package)
    parentReference: ItemReference = field(default_factory=ItemReference)
    size: int | None = None
    specialFolder: SpecialFolder = field(default_factory=SpecialFolder)
    video: Video = field(default_factory=Video)
    webDavUrl: str | None = None
    webUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RemoteItem"
