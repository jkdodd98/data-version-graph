from __future__ import annotations

import typing
from typing import Iterable, Union


class Node:
    def __init__(self, name: str, version: Union[int, str] = 1) -> None:
        self.name = name
        self.version = version
        self.predecessors: list[Node] = []

    @property
    def _node_type(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self._node_type}(name={self.name!r}, version={self.version!r})"

    def __hash__(self) -> int:
        return hash((self.name, self.version))

    def __eq__(self, right: typing.Any) -> bool:
        if isinstance(right, self.__class__):
            return self.name == right.name and self.version == right.version
        return False

    def __rshift__(
        self, right: Union[Node, Iterable[Node]]
    ) -> Union[Node, Iterable[Node]]:
        if isinstance(right, Node):
            right.add_predecessor(self)
            return right
        elif isinstance(right, Iterable) and all(
            isinstance(node, Node) for node in right
        ):
            for node in right:
                node.add_predecessor(self)
            return right
        else:
            raise TypeError("Right operand must be Node or Iterable[Nodes]")

    def __rrshift__(self, left: Iterable[Node]) -> Union[Node, Iterable[Node]]:
        if isinstance(left, Iterable) and all(isinstance(node, Node) for node in left):
            self.add_predecessor(*left)
            return left
        else:
            raise TypeError("Left operand must be Iterable[Nodes]")

    def add_predecessor(self, *nodes: Node) -> None:
        if all(isinstance(node, Node) for node in nodes):
            self.predecessors.extend(
                node for node in nodes if node not in self.predecessors
            )
        else:
            raise TypeError("Can only add Node instances as predecessors")

    def remove_predecessor(self, *nodes: Node) -> None:
        if all(isinstance(node, Node) for node in nodes):
            for node in nodes:
                self.predecessors.remove(node)
        else:
            raise TypeError("Can only remove Node instances as predecessors")

    def predecessor_tree(self, _nodes: set[Node] = None) -> list[Node]:
        if _nodes is None:
            _nodes = set()

        result = []
        for node in self.predecessors:
            if node not in _nodes:
                _nodes.add(node)
                result.append(node)
                result.extend(node.predecessor_tree(_nodes))

        return result
