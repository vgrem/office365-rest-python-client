from office365.runtime.paths.v4.entity import EntityPath


class ChildrenPath(EntityPath):
    """Resource path for OneDrive children addressing"""

    def __init__(self, parent, collection=None):
        super().__init__("children", parent, collection)

    @property
    def collection(self):
        if self._collection is None:
            if isinstance(self.parent, EntityPath):
                # The parent is an entity; its canonical collection is either
                # explicit (e.g. ``RootPath.collection`` -> ``/.../items``) or,
                # for an entity addressed as ``EntityPath(id, collection)``, the
                # collection is the entity's own parent (``.../items``). Without
                # this fallback a nested ``.../children`` collapses to ``None``
                # and the next segment resolves to a bare ``/{id}``.
                self._collection = self.parent.collection or self.parent.parent
            else:
                self._collection = self.parent
        coll = self._collection
        while isinstance(coll, ChildrenPath):
            coll = coll.collection
        return coll
