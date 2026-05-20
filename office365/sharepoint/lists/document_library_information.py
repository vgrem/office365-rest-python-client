from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class DocumentLibraryInformation(ClientValue):
    """Specifies the information for a document library on a site.

    Fields:
        Title (str): Identifies the title of the document library
        AbsoluteUrl (str): Absolute Url of the document library.
        ServerRelativeUrl (str): Identifies the server-relative URL of the document library.
        DriveId (str):
        FromCrossFarm (bool):
        IsDefaultDocumentLibrary (bool):
    """

    Title: Optional[str] = None
    AbsoluteUrl: Optional[str] = None
    ServerRelativeUrl: Optional[str] = None
    DriveId: Optional[str] = None
    FromCrossFarm: Optional[bool] = None
    IsDefaultDocumentLibrary: Optional[bool] = None
    Id: Optional[str] = None
    Modified: datetime = datetime.min
    ModifiedFriendlyDisplay: Optional[str] = None
