from __future__ import annotations

import typing
from typing import Iterable, Union


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

    def __rshift__(self, other: Node) -> None:
        if isinstance(other, Node):
            other.add_predecessor(self)
        else:
            raise TypeError("Can only add Node instances as predecessors")

    def add_predecessor(self, *nodes: Node) -> None:
        if all(isinstance(node, Node) for node in nodes):
            self.predecessors.extend(
                node for node in nodes if node not in self.predecessors
            )
        else:
            raise TypeError("Can only add Node instances as predecessors")


if __name__ == "__main__":
    node = Node("test-node")
    node_2 = Node("test-node-2", 2)

    node >> node_2
    print(node.predecessors)
    print(node_2.predecessors)
