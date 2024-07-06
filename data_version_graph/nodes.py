from __future__ import annotations

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
