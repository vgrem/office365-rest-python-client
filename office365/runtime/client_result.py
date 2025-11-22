from __future__ import annotations

import copy
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Generic, Optional, Union

from requests import Response
from typing_extensions import Self

from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.client_value import ClientValueT
from office365.runtime.http.request_options import RequestOptions

if TYPE_CHECKING:
    from office365.runtime.client_runtime_context import ClientRuntimeContext


class ClientResult(Generic[ClientValueT]):
    """Client result"""

    def __init__(
        self,
        context: ClientRuntimeContext,
        default_value: Optional[ClientValueT] = None,
    ) -> None:
        """Client result"""
        self._context = context
        self._value = copy.deepcopy(default_value)  # type: ClientValueT

    def before_execute(self, action: Callable[[RequestOptions], None]) -> Self:
        """Attach an event handler which is triggered before query is submitted to server"""
        self._context.before_query_execute(action)
        return self

    def after_execute(
        self,
        action: Callable[[Union[Self, Response]], None],
        execute_first: bool = False,
        include_response: bool = False,
    ) -> Self:
        """Attach an event handler which is triggered after query is submitted to server"""
        self._context.after_query_execute(action, execute_first, include_response)
        return self

    def set_property(self, key: str, value: Any, persist_changes: bool = False) -> Self:
        from office365.runtime.client_value import ClientValue  # noqa

        if isinstance(self._value, ClientValue):
            self._value.set_property(key, value, persist_changes)
        elif isinstance(self._value, dict):
            self._value[key] = value
        elif isinstance(self._value, Enum):
            enum_type = type(self._value)
            try:
                self._value = enum_type(value)
            except ValueError:
                pass
        else:
            self._value = value
        return self

    @property
    def value(self) -> ClientValueT:
        """Returns the value"""
        return self._value

    def execute_query(self) -> Self:
        """Submit request(s) to the server"""
        self._context.execute_query()
        return self

    def execute_query_retry(
        self,
        max_retry: int = 5,
        timeout_secs: int = 5,
        success_callback: Optional[Callable[[Any], None]] = None,
        failure_callback: Optional[Callable[[int, Exception], None]] = None,
        exceptions: tuple[type[Exception], ...] = (ClientRequestException,),
    ) -> Self:
        """
        Executes the current set of data retrieval queries and method invocations and retries it if needed.


         Args:
            max_retry: Maximum retry attempts
            timeout_secs: Delay between retries in seconds
            success_callback: Called on successful execution
            failure_callback: Called after failed retries
            exceptions: Exception types that trigger retries

         Returns:
            Self for method chaining

        """
        self._context.execute_query_retry(
            max_retry=max_retry,
            timeout_secs=timeout_secs,
            success_callback=success_callback,
            failure_callback=failure_callback,
            exceptions=exceptions,
        )
        return self
