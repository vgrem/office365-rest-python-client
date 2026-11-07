from enum import Enum
from typing import Optional


class BaseType(Enum):
    """Specifies the base type for a list."""

    Unknown = -1

    GenericList = 0
    """Specifies a base type for lists that do not correspond to another base type in this enumeration."""

    DocumentLibrary = 1
    """Specifies a base type for a document library."""

    Unused = 2
    """Reserved. MUST NOT be used."""

    DiscussionBoard = 3
    """Specifies a base type that SHOULD NOT be used, but MAY<2> be used for a discussion board."""

    Survey = 4
    """Enumeration whose values specify a base type for a survey list."""

    Issue = 5
    """Specifies a base type for an issue tracking list."""


def is_document_library(base_type: Optional[int]) -> bool:
    """Whether a list of this base type holds files rather than records.

    ``DocumentLibrary`` is the only base type whose items carry a file behind them --
    the distinction a caller makes to decide whether an item's ``FileRef`` is a document
    or a row. Answers for a base type read off a live list and for one replayed out of a
    structure snapshot, which is why it is a function and not only
    :attr:`~office365.sharepoint.lists.list.List.is_document_library`.
    """
    return base_type == BaseType.DocumentLibrary.value
