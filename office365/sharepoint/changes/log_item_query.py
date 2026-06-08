from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ChangeLogItemQuery(ClientValue):
    """Specifies an object that is used as the input parameter of
    GetListItemChangesSinceToken (section 3.2.5.79.2.1.7) method.

    Args:
        change_token (str): Specifies a string that contains the change token for the request.
        query (str): Specifies which records from the list are to be returned and the order in which they will be
            returned. See section 2.2 in [MS-WSSCAML].
        query_options (str): Specifies various options for modifying the Query (section 3.2.5.183.1.1.3).
            See [MS-LISTSWS] section 2.2.4.4.
        contains (str): Specifies a string representation of the XML element that defines custom filtering for the
            query. See [MS-LISTSWS] section 2.2.4.3.
        row_limit (int): Specifies a limit for the number of items in the query that are returned per page.
    """

    Query: Optional[str] = None
    QueryOptions: Optional[str] = None
    ChangeToken: Optional[str] = None
    Contains: Optional[str] = None
    RowLimit: Optional[str] = None
    ViewFields: Optional[str] = None
    ViewName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.ChangeLogItemQuery"
