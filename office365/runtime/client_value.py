from enum import Enum
from typing import Any, Dict, Iterator, Optional, Tuple, TypeVar, Union

from typing_extensions import Self

from office365.runtime.odata.json_format import ODataJsonFormat
from office365.runtime.odata.v3.json_light_format import JsonLightFormat

ClientValueT = TypeVar("ClientValueT", int, float, str, bytes, bool, "ClientValue")


class ClientValue:
    """Represent complex type.
    Complex types consist of a list of properties with no key, and can therefore only exist as properties of a
    containing entity or as a temporary value
    """

    def set_property(
        self, k: Union[str, int], v: Any, persist_changes: bool = True
    ) -> Self:
        prop_val = getattr(self, k, None)
        if isinstance(prop_val, ClientValue) and v is not None:
            if isinstance(v, list):
                [
                    prop_val.set_property(i, p_v, persist_changes)
                    for i, p_v in enumerate(v)
                ]
            else:
                [prop_val.set_property(k, p_v, persist_changes) for k, p_v in v.items()]
            setattr(self, k, prop_val)
        else:
            setattr(self, k, v)
        return self

    def get_property(self, name: str) -> ClientValueT:
        """Gets a property value.

        Args:
            name: Name of the property to retrieve

        Returns:
            The property value

        Raises:
            AttributeError: If property doesn't exist
        """
        return getattr(self, name)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for n, v in vars(self).items():
            yield n, v

    def to_json(self, json_format: Optional[ODataJsonFormat] = None) -> Dict[str, Any]:
        """Serializes the ClientValue to JSON format.

        Args:
            json_format: Optional OData JSON formatting options

        Returns:
            Dictionary representing the JSON-serialized object
        """

        def _is_valid_value(val):
            from office365.runtime.client_value_collection import ClientValueCollection

            if val is None:
                return False
            elif isinstance(val, ClientValueCollection) and len(val) == 0:
                return False
            return True

        json = {k: v for k, v in self if _is_valid_value(v)}
        for n, v in json.items():
            if isinstance(v, ClientValue):
                json[n] = v.to_json(json_format)
            elif isinstance(v, Enum):
                json[n] = v.value
        if (
            json_format is not None
            and json_format.include_control_information
            and self.entity_type_name is not None
        ):
            if isinstance(json_format, JsonLightFormat):
                json[json_format.metadata_type] = {"type": self.entity_type_name}
            elif isinstance(json_format, ODataJsonFormat):
                json[json_format.metadata_type] = "#" + self.entity_type_name
        return json

    @property
    def entity_type_name(self) -> Optional[str]:
        """The server-side type name for client value.

        Returns:
            Defaults to the class name
        """
        # return type(self).__name__
        return None
