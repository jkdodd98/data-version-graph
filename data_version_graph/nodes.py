from __future__ import annotations

import typing
from typing import Union


class Node:
    def __init__(self, name: str, version: Union[int, str] = 1) -> None:
        self.name = name
        self.version = version
        self.predecessors = []

    @property
    def _node_type(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self._node_type}(name={self.name!r}, version={self.version!r})"

    def __eq__(self, other: typing.Any) -> bool:
        if isinstance(other, self.__class__):
            return self.name == other.name and self.version == other.version
        return False

    def add_predecessor(self, *nodes: Node) -> None:
        self.predecessors.extend(
            node for node in nodes if node not in self.predecessors
        )
