from enum import Enum


class SPModerationStatusType(Enum):
    """The approval status of a list item.

    The values are the ``CHOICES`` the ``_ModerationStatus`` column declares:
    ``0;#Approved``, ``1;#Rejected``, ``2;#Pending``, ``3;#Draft``, ``4;#Scheduled``.
    """

    Approved = 0
    Rejected = 1
    Pending = 2
    Draft = 3
    Scheduled = 4
