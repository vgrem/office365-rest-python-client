from __future__ import annotations

from office365.entity_collection import EntityCollection
from office365.runtime.query_capabilities import query_capabilities
from office365.security.article import Article

_DOC = "https://learn.microsoft.com/en-us/graph/api/security-threatintelligence-list-articles"


@query_capabilities(
    unsupported={"filter"},
    doc=_DOC,
    note="the threat intelligence articles feed rejects every $filter it was asked for",
)
class ArticleCollection(EntityCollection[Article]):
    """Represents a collection of threat intelligence articles.

    Measured on the feed: ``tags/any(t:t eq 'malware')``, ``contains(tags,'malware')`` and
    even ``createdDateTime ge ...`` all answer 400 ``invalidRequest``, while ``$top`` and
    ``$select`` answer 200 - so there is no server-side filter to declare as supported.
    """

    def __init__(self, context, resource_path=None):
        super().__init__(context, Article, resource_path)
