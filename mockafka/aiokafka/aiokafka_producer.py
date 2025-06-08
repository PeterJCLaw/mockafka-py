from __future__ import annotations

import asyncio
from typing import Any, Optional

from aiokafka.util import create_future  # type: ignore[import-untyped]
from typing_extensions import LiteralString, Self

from mockafka.kafka_store import KafkaStore
from mockafka.message import Message, HeadersList


def _check_type(obj: object, name: LiteralString) -> None:
    if not (
        obj is None or isinstance(obj, bytes)
    ):
        # Match apparent behaviour of `aiokafka.AIOKafkaProducer`
        raise ValueError(f"{name} must be bytes or None, not {type(obj)}")


class FakeAIOKafkaProducer:
    """
    FakeAIOKafkaProducer is a mock implementation of aiokafka's AIOKafkaProducer.

    It allows mocking a kafka producer for testing purposes.

    Parameters:
    - args, kwargs: Passed to superclass init, not used here.

    Attributes:
    - kafka: KafkaStore instance for underlying storage.

    Methods:
    - _produce(): Create a Message and produce to KafkaStore.
      Takes topic, value, and optional partition.
    - start(): No-op.
    - stop(): No-op.
    - send(): Call _produce() with kwargs.
    - send_and_wait(): Call send().
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.kafka = KafkaStore()

    async def _produce(
        self,
        topic: str,
        value: Optional[bytes],
        key: Optional[bytes],
        partition: int,
        timestamp_ms: Optional[int] = None,
        headers: Optional[HeadersList] = None,
    ) -> None:
        # create a message and call produce kafka
        message = Message(
            topic=topic,
            value=value,
            key=key,
            partition=partition,
            timestamp=timestamp_ms,
            headers=headers,
        )
        self.kafka.produce(message=message, topic=topic, partition=partition)

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass

    async def send(
        self,
        topic: str,
        value: Optional[bytes] = None,
        key: Optional[bytes] = None,
        partition: int = 0,
        timestamp_ms: Optional[int] = None,
        headers: Optional[HeadersList] = None,
    ) -> asyncio.Future[None]:
        await self._produce(
            topic=topic,
            value=value,
            key=key,
            partition=partition,
            headers=headers,
            timestamp_ms=timestamp_ms,
        )
        future: asyncio.Future[None] = create_future()
        future.set_result(None)
        return future

    async def send_and_wait(
        self,
        topic: str,
        value: Optional[bytes] = None,
        key: Optional[bytes] = None,
        partition: int = 0,
        timestamp_ms: Optional[int] = None,
        headers: Optional[HeadersList] = None,
    ) -> None:
        future = await self.send(
            topic=topic,
            value=value,
            key=key,
            partition=partition,
            headers=headers,
            timestamp_ms=timestamp_ms,
        )
        return await future

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(
        self,
        exception_type: object,
        exception: object,
        traceback: object,
    ) -> None:
        await self.stop()
