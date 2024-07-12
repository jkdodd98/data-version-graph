import networkx as nx
import pytest

from data_version_graph.graph import Graph
from data_version_graph.nodes import Node


class TestGraph:
    def setup_method(self):
        self.graph = Graph()
        self.graph2 = Graph()
        self.node = Node("test")
        self.node2 = Node("test2")
        self.node3 = Node("test3")
        self.node4 = Node("test", version=2)

    def teardown_method(self):
        del self.graph
        del self.graph2

    def test_init(self):
        assert hasattr(self.graph, "graph")
        assert isinstance(self.graph.graph, nx.DiGraph)
        assert list(self.graph.graph.nodes) == []
        assert hasattr(self.graph2, "graph")
        assert isinstance(self.graph2.graph, nx.DiGraph)
        assert list(self.graph.graph.nodes) == []

    def test_add_node(self):
        self.graph.add_node(self.node)
        assert self.node in self.graph.graph.nodes
        assert list(self.graph.graph.nodes) == [self.node]

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
        self.graph.add_edge(self.node, self.node2)
        assert self.graph.graph.has_node(self.node)
        assert self.graph.graph.has_node(self.node2)
        assert self.graph.graph.has_edge(self.node, self.node2)

        self.graph.add_edge(self.node2, self.node3)
        assert self.graph.graph.has_node(self.node3)
        assert self.graph.graph.has_edge(self.node2, self.node3)

        with pytest.raises(ValueError, match="Adding this edge would create a cycle"):
            self.graph.add_edge(self.node3, self.node)

        with pytest.raises(
            TypeError, match="Only instances of Node can be added to the graph"
        ):
            self.graph.add_edge("test", self.node)

        with pytest.raises(
            TypeError, match="Only instances of Node can be added to the graph"
        ):
            self.graph.add_edge(self.node, "test")

        with pytest.raises(
            TypeError, match="Only instances of Node can be added to the graph"
        ):
            self.graph.add_edge("test", "test2")

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
