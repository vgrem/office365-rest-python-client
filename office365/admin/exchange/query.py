from __future__ import annotations

from typing import Any, Dict, Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.client_query import ClientQuery


class CmdletQuery(ClientQuery):
    """One cmdlet call: ``POST <root>/<endpoint>`` with a ``CmdletInput`` envelope.

    The API has no entity paths, so this replaces the OData read/create/update/delete queries.
    ``next_link`` is filled from ``@odata.nextLink`` after execution.
    """

    def __init__(
        self,
        context,
        endpoint: str,
        cmdlet: str,
        parameters: Optional[Dict[str, Any]] = None,
        anchor: Optional[str] = None,
        select: Optional[list[str]] = None,
        next_link: Optional[str] = None,
        return_type: Optional[ClientResult] = None,
        single: bool = False,
    ) -> None:
        super().__init__(context, return_type=return_type if return_type is not None else ClientResult(context))
        self.endpoint = endpoint
        self.cmdlet = cmdlet
        self.parameters = dict(parameters or {})
        self.anchor = anchor
        self.select = list(select or [])
        self.next_link = next_link
        #: A cmdlet answers a collection even when it returns one object; ``single`` keeps the object.
        self.single = single
        # Each cmdlet is its own POST; nothing here can ride in a Graph-style batch.
        self.batchable = False

    @property
    def result(self) -> ClientResult:
        """The result object this query fills; a cmdlet call always has one."""
        return self.return_type  # type: ignore[return-value]

    def body(self) -> Dict[str, Any]:
        cmdlet_input: Dict[str, Any] = {"CmdletName": self.cmdlet}
        if self.parameters:
            cmdlet_input["Parameters"] = self.parameters
        return {"CmdletInput": cmdlet_input}
