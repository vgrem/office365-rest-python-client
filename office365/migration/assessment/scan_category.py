from enum import Enum


class ScanCategory(Enum):
    """Granularity of a scan report — mirrors SMAT's ``ReportCategoryType``."""

    SPSITE = "SPSite"
    SPWEB = "SPWeb"
    SPLIST = "SPList"
    SPLISTITEM = "SPListItem"
    SPFILE = "SPFile"
