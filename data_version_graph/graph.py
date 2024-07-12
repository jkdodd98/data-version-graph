from typing import TYPE_CHECKING, Optional

import networkx as nx

from .nodes import Node

if TYPE_CHECKING:
    from .nodes import Node  # pragma: no cover


class Graph:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_node(self, node: "Node") -> None:
        if not isinstance(node, Node):
            raise TypeError("Only instances of Node can be added to the graph")
        self.graph.add_node(node)

    def remove_node(self, node: "Node") -> None:
        if not isinstance(node, Node):
            raise TypeError("Only instances of Node can be removed from the graph")
        self.graph.remove_node(node)

    def add_edge(self, from_node: "Node", to_node: "Node") -> None:
        if not all(isinstance(node, Node) for node in (from_node, to_node)):
            raise TypeError("Only instances of Node can be added to the graph")
        if self.is_cyclic_with_edge(from_node, to_node):
            raise ValueError("Adding this edge would create a cycle")
        self.graph.add_edge(from_node, to_node)

    def remove_edge(self, from_node: "Node", to_node: "Node") -> None:
        if not all(isinstance(node, Node) for node in (from_node, to_node)):
            raise TypeError("Only instances of Node can be removed from the graph")
        self.graph.remove_edge(from_node, to_node)

    def is_cyclic_with_edge(self, from_node: "Node", to_node: "Node") -> bool:
        self.graph.add_edge(from_node, to_node)
        is_cyclic = not nx.is_directed_acyclic_graph(self.graph)
        self.graph.remove_edge(from_node, to_node)
        return is_cyclic

    def get_node(self, name: str, *, version: int = 1) -> Optional["Node"]:
        for node in self.graph.nodes:
            if isinstance(node, Node) and node.name == name and node.version == version:
                return node
        return None

    def get_latest_version(self, name: str) -> Optional["Node"]:
        nodes: list[Node] = [node for node in self.graph.nodes if node.name == name]
        if not nodes:
            return None
        return max(nodes, key=lambda node: node.version)
