from typing import TYPE_CHECKING, Optional

import networkx as nx
from sqlalchemy.orm import Session

from data_version_graph.database import EdgeModel, NodeModel
from data_version_graph.node_factory import NodeFactory
from data_version_graph.nodes import Node

if TYPE_CHECKING:
    from data_version_graph.nodes import Node  # pragma: no cover


class Graph:
    def __init__(self, session: Session) -> None:
        self.graph = nx.DiGraph()
        self.session = session
        self._load_graph()

    def _load_graph(self) -> None:
        # Load nodes from the database and add them to the graph.
        nodes = self.session.query(NodeModel).all()
        for node in nodes:
            self.add_node(
                NodeFactory.create(node.ntype, name=node.name, version=node.version)
            )

        # Load edges from the database and add them to the graph.
        edges = self.session.query(EdgeModel).all()
        for edge in edges:
            from_node = self._get_db_node_by_id(edge.from_node_id)
            to_node = self._get_db_node_by_id(edge.to_node_id)
            if from_node is not None and to_node is not None:
                self.add_edge(
                    NodeFactory.create(
                        from_node.ntype, name=from_node.name, version=from_node.version
                    ),
                    NodeFactory.create(
                        to_node.ntype, name=to_node.name, version=to_node.version
                    ),
                )

    def add_node(self, node: "Node") -> None:
        if not isinstance(node, Node):
            raise TypeError("Only instances of Node can be added to the graph")
        self.graph.add_node(node, color=node.color)
        self._add_db_node(node)

    def _add_db_node(self, node: "Node") -> None:
        db_node = NodeModel(ntype=node.ntype, name=node.name, version=node.version)
        self.session.add(db_node)  # add the node to the database
        self.session.commit()

    def remove_node(self, node: "Node") -> None:
        if not isinstance(node, Node):
            raise TypeError("Only instances of Node can be removed from the graph")
        if node not in self.graph.nodes:
            return
        self.graph.remove_node(node)
        self._remove_db_node(node)

    def _remove_db_node(self, node: "Node") -> None:
        db_node = self._get_db_node(node.name, version=node.version)
        if db_node is not None:
            self.session.delete(db_node)
            self.session.commit()

    def add_edge(self, from_node: "Node", to_node: "Node") -> None:
        if not all(isinstance(node, Node) for node in (from_node, to_node)):
            raise TypeError("Only instances of Node can be added to the graph")
        if self.is_cyclic_with_edge(from_node, to_node):
            raise ValueError("Adding this edge would create a cycle")

        # This check ensures that the nodes are in the graph before adding the edge.
        for node in (from_node, to_node):
            if self._get_db_node(node.name, version=node.version) is None:
                self.add_node(node)

        self.graph.add_edge(from_node, to_node)
        self._add_db_edge(from_node, to_node)

    def _add_db_edge(self, from_node: "Node", to_node: "Node") -> None:
        db_from_node = self._get_db_node(from_node.name, version=from_node.version)
        db_to_node = self._get_db_node(to_node.name, version=to_node.version)

        if db_to_node is not None and db_from_node is not None:
            db_edge = EdgeModel(from_node_id=db_from_node.id, to_node_id=db_to_node.id)
            self.session.add(db_edge)  # add the edge to the database
            self.session.commit()

    def remove_edge(self, from_node: "Node", to_node: "Node") -> None:
        if not all(isinstance(node, Node) for node in (from_node, to_node)):
            raise TypeError("Only instances of Node can be removed from the graph")
        if (from_node, to_node) not in self.graph.edges:
            return
        self.graph.remove_edge(from_node, to_node)
        self._remove_db_edge(from_node, to_node)

    def _remove_db_edge(self, from_node: "Node", to_node: "Node") -> None:
        db_from_node = self._get_db_node(from_node.name, version=from_node.version)
        db_to_node = self._get_db_node(to_node.name, version=to_node.version)

        if db_to_node is not None and db_from_node is not None:
            db_edge = self._get_db_edge(db_from_node, db_to_node)
            if db_edge:
                self.session.delete(db_edge)
                self.session.commit()

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

    def _get_db_node(self, name: str, *, version: int = 1) -> Optional[NodeModel]:
        return (
            self.session.query(NodeModel).filter_by(name=name, version=version).first()
        )

    def _get_db_node_by_id(self, node_id: int) -> Optional[NodeModel]:
        return self.session.query(NodeModel).filter_by(id=node_id).first()

    def _get_db_edge(
        self, from_node: NodeModel, to_node: NodeModel
    ) -> Optional[EdgeModel]:
        return (
            self.session.query(EdgeModel)
            .filter_by(from_node_id=from_node.id, to_node_id=to_node.id)
            .first()
        )

    def get_latest_version(self, name: str) -> Optional["Node"]:
        nodes: list[Node] = [node for node in self.graph.nodes if node.name == name]
        if not nodes:
            return None
        return max(nodes, key=lambda node: node.version)
