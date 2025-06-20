from dataclasses import dataclass
from typing import Optional


@dataclass
class ODataParameter:
    """Represents a parameter in an OData operation (function/action).

    Attributes:
        Name: The name of the parameter as defined in the OData metadata.
              This should match exactly with the server's expected parameter name.

        ParameterTypeFullName: The fully qualified type name of the parameter.
                              Format is "Namespace.Type" (e.g., "Edm.String").
                              Used for type checking and serialization.
    """

    Name: Optional[str] = None
    ParameterTypeFullName: Optional[str] = None
