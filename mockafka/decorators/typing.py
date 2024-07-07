from __future__ import annotations

from typing import Any, Callable, TypedDict, TypeVar

from typing_extensions import NotRequired

TCallable = TypeVar("TCallable", bound=Callable[..., Any])


class MessageDict(TypedDict):
    value: NotRequired[str]
    key: NotRequired[str]
    topic: NotRequired[str]
    partition: NotRequired[int]
    timestamp: NotRequired[int]
    headers: NotRequired[dict]


class TopicConfig(TypedDict):
    topic: str
    partition: int
