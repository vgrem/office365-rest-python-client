"""OData metadata type names -> Python model annotation formatting (codegen side)."""

from __future__ import annotations

from office365.runtime.odata.type import ODataType


def client_type_name(type_name: str | None, is_object_type: bool = False) -> str:
    """Formats an OData type name as the Python annotation name.

    Examples:
        ``Edm.Int32`` -> ``int``; ``Collection(Edm.String)`` ->
        ``ClientValueCollection[str]``; ``SP.Web`` -> ``Web``;
        ``Collection(SP.Web)`` -> ``EntityCollection[Web]``.
    """
    if type_name is None:
        return ""
    primitive_type = ODataType.primitive_type_for(type_name)
    if primitive_type is not None:
        return primitive_type.__name__
    if ODataType.is_collection_name(type_name):
        item_name = item_client_type_name(ODataType.strip_collection(type_name), is_object_type)
        if is_object_type:
            return f"EntityCollection[{item_name}]"
        return f"ClientValueCollection[{item_name}]"
    cls_name = type_name.split(".")[-1]
    if cls_name and cls_name[0].islower():
        cls_name = cls_name[0].upper() + cls_name[1:]
    return cls_name


def item_client_type_name(type_name: str | None, is_object_type: bool = False) -> str:
    """Formats the item type of a collection (or the type itself) as a Python name."""
    return client_type_name(ODataType.strip_collection(type_name), is_object_type)
