from __future__ import annotations

import time
from typing import Optional

from confluent_kafka import (  # type: ignore[import-untyped]
    TIMESTAMP_CREATE_TIME,
    TIMESTAMP_LOG_APPEND_TIME,
    TIMESTAMP_NOT_AVAILABLE,
    KafkaError,
)

HeadersList = list[tuple[str, Optional[bytes]]]


class Message:
    def __init__(
        self,
        headers: Optional[HeadersList] = None,
        key: Optional[bytes] = None,
        value: Optional[bytes] = None,
        topic: Optional[str] = None,
        offset: Optional[int] = None,
        error: Optional[KafkaError] = None,
        latency: Optional[float] = None,
        leader_epoch: Optional[int] = None,
        partition: Optional[int] = None,
        timestamp: Optional[int] = None,
        timestamp_type: int = TIMESTAMP_CREATE_TIME,
        broker_receive_time: Optional[int] = None,
    ) -> None:
        self._headers = headers
        self._key = key
        self._value = value
        self._topic = topic
        self._offset = offset
        self._error = error
        self._latency = latency
        self._leader_epoch = leader_epoch
        self._partition = partition
        self._timestamp: int = timestamp or int(time.time() * 1000)
        self._timestamp_type = timestamp_type
        self._broker_receive_time = broker_receive_time or int(time.time() * 1000)

    def offset(self, *args, **kwargs) -> Optional[int]:
        return self._offset

    def latency(self, *args, **kwargs) -> Optional[float]:
        return self._latency

    def leader_epoch(self, *args, **kwargs) -> Optional[int]:
        return self._leader_epoch

    def headers(self) -> Optional[HeadersList]:
        return self._headers

    def key(self, *args, **kwargs) -> Optional[bytes]:
        return self._key

    def value(self, *args, **kwargs) -> Optional[bytes]:
        return self._value

    def timestamp(self, *args, **kwargs) -> tuple[int, int]:
        ts_info: tuple[int, int]
        if self._timestamp_type == TIMESTAMP_NOT_AVAILABLE:
            ts_info = (TIMESTAMP_NOT_AVAILABLE, 0)
        elif self._timestamp_type == TIMESTAMP_LOG_APPEND_TIME:
            ts_info = (TIMESTAMP_LOG_APPEND_TIME, self._broker_receive_time)
        else:
            ts_info = (self._timestamp_type, self._timestamp)
        return ts_info

    def topic(self, *args, **kwargs) -> Optional[str]:
        return self._topic

    def partition(self, *args, **kwargs) -> Optional[int]:
        return self._partition

    def error(self) -> Optional[KafkaError]:
        return self._error

    def set_headers(self, *args, **kwargs):  # real signature unknown
        pass

    def set_key(self, *args, **kwargs):  # real signature unknown
        pass

    def set_value(self, *args, **kwargs):  # real signature unknown
        pass
