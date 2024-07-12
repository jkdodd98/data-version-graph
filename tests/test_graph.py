import networkx as nx
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from data_version_graph.database import Base
from data_version_graph.graph import Graph
from data_version_graph.nodes import Node


class TestGraph:
    def setup_method(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.graph = Graph(session=self.session)
        self.node = Node("test")
        self.node2 = Node("test2")
        self.node3 = Node("test3")
        self.node4 = Node("test", version=2)

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

        del self.graph
        del self.node
        del self.node2
        del self.node3
        del self.node4

    def test_init(self):
        assert hasattr(self.graph, "graph")
        assert isinstance(self.graph.graph, nx.DiGraph)
        assert hasattr(self.graph, "session")
        assert isinstance(self.graph.session, Session)
        assert list(self.graph.graph.nodes) == []

    def test__load_graph(self):
        self.graph.add_node(self.node)
        self.graph.add_node(self.node2)
        self.graph.add_edge(self.node, self.node2)

        graph = Graph(session=self.session)
        assert list(graph.graph.nodes) == [self.node, self.node2]
        assert graph.graph.nodes == self.graph.graph.nodes
        assert list(graph.graph.edges) == list(self.graph.graph.edges)

    def test_add_node(self):
        self.graph.add_node(self.node)
        assert self.node in self.graph.graph.nodes
        assert list(self.graph.graph.nodes) == [self.node]
        assert (
            self.graph._get_db_node(self.node.name, version=self.node.version)
            is not None
        )

        with pytest.raises(
            TypeError, match="Only instances of Node can be added to the graph"
        ):
            self.graph.add_node("test")

    def test_remove_node(self):
        self.graph.add_node(self.node)
        assert self.node in self.graph.graph.nodes

        self.graph.remove_node(self.node)
        assert self.node not in self.graph.graph.nodes

        with pytest.raises(
            TypeError, match="Only instances of Node can be removed from the graph"
        ):
            self.graph.remove_node("test")

    def test_add_edge(self):
        # test adding an edge between two nodes.
        self.graph.add_node(self.node)
        self.graph.add_node(self.node2)
        self.graph.add_edge(self.node, self.node2)
        assert (self.node, self.node2) in self.graph.graph.edges

        # test adding an edge between a Node and a not Node.
        with pytest.raises(
            TypeError, match="Only instances of Node can be added to the graph"
        ):
            self.graph.add_edge(self.node, "not_a_node")

        # test adding an edge that creates a cycle.
        with pytest.raises(ValueError, match="Adding this edge would create a cycle"):
            self.graph.add_edge(self.node2, self.node)

        # test adding a duplicate edge.
        self.graph.add_edge(self.node, self.node2)
        assert (self.node, self.node2) in self.graph.graph.edges
        assert len(self.graph.graph.edges) == 1

        # test adding an edge to Node not in Graph.
        self.graph.add_edge(self.node, self.node4)
        assert (self.node, self.node4) in self.graph.graph.edges
        assert len(self.graph.graph.edges) == 2
        assert self.node4 in self.graph.graph.nodes
        assert (
            self.graph._get_db_node(self.node4.name, version=self.node4.version)
            is not None
        )

    def test_remove_edge(self):
        self.graph.add_edge(self.node, self.node2)
        self.graph.add_edge(self.node2, self.node3)
        assert self.graph.graph.has_edge(self.node, self.node2)
        assert self.graph.graph.has_edge(self.node2, self.node3)

        self.graph.remove_edge(self.node, self.node2)
        assert not self.graph.graph.has_edge(self.node, self.node2)
        assert list(self.graph.graph.edges) == [(self.node2, self.node3)]

        with pytest.raises(
            TypeError, match="Only instances of Node can be removed from the graph"
        ):
            self.graph.remove_edge("test", self.node)

        with pytest.raises(
            TypeError, match="Only instances of Node can be removed from the graph"
        ):
            self.graph.remove_edge(self.node, "test")

        with pytest.raises(
            TypeError, match="Only instances of Node can be removed from the graph"
        ):
            self.graph.remove_edge("test", "test1")

    def test_is_cyclic_with_edge(self):
        self.graph.add_edge(self.node, self.node2)
        assert self.graph.is_cyclic_with_edge(self.node2, self.node)
        assert not self.graph.is_cyclic_with_edge(self.node, self.node3)
        assert not self.graph.is_cyclic_with_edge(self.node3, self.node)

        self.graph.add_edge(self.node2, self.node3)
        assert not self.graph.is_cyclic_with_edge(self.node, self.node3)
        assert self.graph.is_cyclic_with_edge(self.node3, self.node)

    def test_get_node(self):
        self.graph.add_node(self.node)
        self.graph.add_node(self.node4)
        assert self.graph.get_node("test") == self.node
        assert self.graph.get_node("test", version=2) == self.node4
        assert self.graph.get_node("test", version=3) is None

    def test_get_latest_version(self):
        self.graph.add_node(self.node)
        self.graph.add_node(self.node2)
        assert self.graph.get_latest_version("test") == self.node
        assert self.graph.get_latest_version("test2") == self.node2

        self.graph.add_node(self.node4)
        assert self.graph.get_latest_version("test") == self.node4
        assert self.graph.get_latest_version("test2") == self.node2
        assert self.graph.get_latest_version("test3") is None
