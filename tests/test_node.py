import pytest

from data_version_graph.nodes import Node


def test_node_init() -> None:
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


def test_node_node_type() -> None:
    node = Node("test-node")
    assert node._node_type == "Node"

    node_2 = Node("test-node-2", 2)
    assert node_2._node_type == "Node"


def test_node_repr() -> None:
    node = Node("test-node")
    assert repr(node) == "Node(name='test-node', version=1)"

    node_2 = Node("test-node-2", 2)
    assert repr(node_2) == "Node(name='test-node-2', version=2)"

    node_3 = Node("test-node-3", "1.0.0")
    assert repr(node_3) == "Node(name='test-node-3', version='1.0.0')"

    node_4 = Node("test-node-4", "3")
    assert repr(node_4) == "Node(name='test-node-4', version='3')"


def test_node_hash() -> None:
    node = Node("test-node")
    node_2 = Node("test-node-2", 2)
    node_3 = Node("test-node-3", "1.0.0")
    node_4 = Node("test-node-3", "1.0.0")

    assert hash(node) == hash(("test-node", 1))
    assert hash(node_2) == hash(("test-node-2", 2))
    assert hash(node_3) == hash(("test-node-3", "1.0.0"))
    assert hash(node_3) == hash(node_4)


def test_node_eq() -> None:
    node = Node("test-node")
    node_2 = Node("test-node", 2)
    node_3 = Node("test-node-2", "1.0.0")
    node_4 = Node("test-node-2", "1.0.0")

    assert node == Node("test-node")
    assert node_2 == Node("test-node", 2)
    assert node_3 == Node("test-node-2", "1.0.0")
    assert node_3 == node_4
    assert node != node_2
    assert node != node_3

    assert node != "test-node"


def test_node_add_predecessors() -> None:
    node = Node("test-node")
    node_2 = Node("test-node-2", 2)
    node_3 = Node("test-node-3", "1.0.0")

    node_2.add_predecessor(node)
    assert node_2.predecessors == [node]

    node_3.add_predecessor(node, node_2)
    assert node_3.predecessors == [node, node_2]

    with pytest.raises(TypeError):
        node_3.add_predecessor("test-node")


def test_node_rshift() -> None:
    node = Node("test-node")
    node_2 = Node("test-node-2", 2)
    node_3 = Node("test-node-3", "1.0.0")
    node_4 = Node("test-node-2", 2)
    node_5 = Node("test-node-5")
    node_6 = Node("test-node-6")

    node >> node_2
    assert node_2.predecessors == [node]

    node >> node_3
    node_2 >> node_3
    assert node_3.predecessors == [node, node_2]

    node_4 >> node_3
    assert node_3.predecessors == [node, node_2]

    node_4 >> node_5 >> node_6
    assert node_5.predecessors == [node_4]
    assert node_6.predecessors == [node_5]


def test_node_rrshift() -> None:
    node = Node("test-node")
    node_2 = Node("test-node-2", 2)
    node_3 = Node("test-node-3", "1.0.0")
    node_4 = Node("test-node-2", 2)

    [node, node_2, node_4] >> node_3
    assert node_3.predecessors == [node, node_2]

    node_A = Node("test-node-A")
    node_B = Node("test-node-B")
    node_C = Node("test-node-C")
    node_D = Node("test-node-D")
    node_E = Node("test-node-E")

    node_A >> [node_B, node_C] >> node_D
    assert node_A.predecessors == []
    assert node_B.predecessors == [node_A]
    assert node_C.predecessors == [node_A]
    assert node_D.predecessors == [node_B, node_C]

    (node_A, node_B) >> node_E
    assert node_E.predecessors == [node_A, node_B]
