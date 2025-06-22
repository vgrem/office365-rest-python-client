from typing import Dict, Optional

from office365.runtime.paths.service_operation import ServiceOperationPath


class StaticOperationPath(ServiceOperationPath):
    def __init__(self, static_name: str, parameters: Optional[Dict] = None) -> None:
        super(StaticOperationPath, self).__init__(static_name, parameters)
