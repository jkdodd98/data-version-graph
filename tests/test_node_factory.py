import pytest

from data_version_graph.node_factory import NodeFactory
from data_version_graph.nodes import (
    BigQueryTable,
    GoogleCloudStorageObject,
    Node,
    PostgresTable,
)


class TestNodeFactory:
    def test_create(self):
        node = NodeFactory.create("Node", name="test")
        assert isinstance(node, Node)
        assert node.name == "test"
        assert node.version == 1
        assert node.ntype == "Node"

        node = NodeFactory.create("Node", name="test", version=2)
        assert isinstance(node, Node)
        assert node.name == "test"
        assert node.version == 2
        assert node.ntype == "Node"

        node = NodeFactory.create("BigQueryTable", name="test")
        assert isinstance(node, BigQueryTable)
        assert node.name == "test"
        assert node.version == 1
        assert node.ntype == "BigQueryTable"

        node = NodeFactory.create("PostgresTable", name="test")
        assert isinstance(node, PostgresTable)
        assert node.name == "test"
        assert node.version == 1
        assert node.ntype == "PostgresTable"

        node = NodeFactory.create("GoogleCloudStorageObject", name="test")
        assert isinstance(node, GoogleCloudStorageObject)
        assert node.name == "test"
        assert node.version == 1
        assert node.ntype == "GoogleCloudStorageObject"

        with pytest.raises(ValueError, match="Unknown node type: test"):
            NodeFactory.create("test", name="test")
