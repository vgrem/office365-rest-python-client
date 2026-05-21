from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.directory.insights.identity import InsightIdentity
from office365.directory.insights.resource_reference import ResourceReference
from office365.runtime.client_value import ClientValue


@dataclass
class SharingDetail(ClientValue):
    """Complex type containing properties of sharedInsight items.

    :param datetime shared_datetime: The date and time the file was last shared.
    :param ResourceReference sharing_reference:
    :param str sharing_subject: The subject with which the document was shared.
    :param str sharing_type: Determines the way the document was shared,
        can be by a "Link", "Attachment", "Group", "Site".
    """

    sharedBy: InsightIdentity = field(default_factory=InsightIdentity)
    sharedDateTime: datetime | None = None
    sharingReference: ResourceReference = field(default_factory=ResourceReference)
    sharingSubject: str | None = None
    sharingType: str | None = None
