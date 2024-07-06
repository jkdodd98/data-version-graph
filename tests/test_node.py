from data_version_graph.nodes import Node


def test_node_init():
    node = Node("test-node")
    assert node.name == "test-node"
    assert node.version == 1
    assert node.predecessors == []

    node_2 = Node("test-node-2", 2)
    assert node_2.name == "test-node-2"
    assert node_2.version == 2
    assert node_2.predecessors == []

    node_3 = Node("test-node-3", "1.0.0")
    assert node_3.name == "test-node-3"
    assert node_3.version == "1.0.0"
    assert node_3.predecessors == []


def test_node_node_type():
    node = Node("test-node")
    assert node._node_type == "Node"

    node_2 = Node("test-node-2", 2)
    assert node_2._node_type == "Node"


def test_node_repr():
    node = Node("test-node")
    assert repr(node) == "Node(name='test-node', version=1)"

    node_2 = Node("test-node-2", 2)
    assert repr(node_2) == "Node(name='test-node-2', version=2)"

    node_3 = Node("test-node-3", "1.0.0")
    assert repr(node_3) == "Node(name='test-node-3', version='1.0.0')"

    node_4 = Node("test-node-4", "3")
    assert repr(node_4) == "Node(name='test-node-4', version='3')"
