from abc import ABC, abstractmethod
from typing import Any, Dict, Generic

from typing_extensions import Self

from office365.runtime.client_object import T


class BaseScanner(ABC, Generic[T]):

    def __init__(self, source):
        # type: (T) -> None
        self.source = source
        self._result = {}  # type: Dict[str, Any]

    @abstractmethod
    def build_query(self):
        # type: () -> Self
        pass

    @abstractmethod
    def process(self):
        # type: () -> Dict
        pass

    def scan(self):
        # type: () -> Dict
        self.build_query()
        self.source.execute_query()
        return self.process()
