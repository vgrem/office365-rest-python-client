from typing import Optional

from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.usercustomactions.action import UserCustomAction


class UserCustomActionCollection(EntityCollection[UserCustomAction]):
    def __init__(self, context, resource_path=None):
        """Specifies a collection of custom actions."""
        super().__init__(context, UserCustomAction, resource_path)

    def add(
        self,
        title: str,
        location: str,
        sequence: int = 100,
        script_block: Optional[str] = None,
        script_src: Optional[str] = None,
        url: Optional[str] = None,
        **kwargs,
    ) -> UserCustomAction:
        """Add a new custom action to the collection (deferred — call ``execute_query()`` to submit).

        Args:
            title: The display title of the custom action.
            location: Where the action is added (e.g. ``ScriptLink`` for a site-wide script,
              ``EditControlBlock`` for a list toolbar button).
            sequence: Execution order of the action.
            script_block: ECMAScript to execute on every page (ScriptLink actions).
            script_src: URI of a file containing ECMAScript to execute (ScriptLink actions).
            url: The URL or ECMAScript function associated with the action.
        """
        return_type = UserCustomAction(self.context)
        return_type.set_property("Title", title)
        return_type.set_property("Location", location)
        return_type.set_property("Sequence", sequence)
        if script_block is not None:
            return_type.set_property("ScriptBlock", script_block)
        if script_src is not None:
            return_type.set_property("ScriptSrc", script_src)
        if url is not None:
            return_type.set_property("Url", url)
        for k, v in kwargs.items():
            return_type.set_property(k, v)
        self.add_child(return_type)
        qry = CreateEntityQuery(self, return_type, return_type)
        self.context.add_query(qry)
        return return_type

    def clear(self):
        """
        Deletes all custom actions in the collection.
        Exceptions:
        - 2130575305 Microsoft.SharePoint.SPException Custom action was modified on the server  in a way that
             prevents changes from being committed, as determined by the protocol server.
        """
        qry = ServiceOperationQuery(self, "Clear")
        self.context.add_query(qry)
        return self
