from data_version_graph.nodes import (
    BigQueryTable,
    GoogleCloudStorageObject,
    Node,
    PostgresTable,
)


class TestNode:
    def setup_method(self) -> None:
        self.node = Node(name="test_node")
        self.node2 = Node(name="test_node2")
        self.node3 = Node(name="test_node", version=2)

    def teardown_method(self) -> None:
        del self.node
        del self.node2
        del self.node3

    def test_init(self) -> None:
        assert self.node.name == "test_node"
        assert self.node.version == 1
        assert self.node2.name == "test_node2"
        assert self.node2.version == 1
        assert self.node3.name == "test_node"
        assert self.node3.version == 2

    def test_repr(self) -> None:
        assert repr(self.node) == "Node(name='test_node', version=1)"
        assert repr(self.node2) == "Node(name='test_node2', version=1)"
        assert repr(self.node3) == "Node(name='test_node', version=2)"

    def test_eq(self) -> None:
        assert self.node == Node(name="test_node")
        assert self.node != Node(name="test_node2")
        assert self.node != Node(name="test_node", version=2)
        assert self.node != "test_node"
        assert self.node != self.node2
        assert self.node3 == Node(name="test_node", version=2)

    def test_hash(self) -> None:
        assert hash(self.node) == hash(("Node", "test_node", 1))
        assert hash(self.node2) == hash(("Node", "test_node2", 1))
        assert hash(self.node3) == hash(("Node", "test_node", 2))


class TestBigQueryTable:
    def setup_method(self) -> None:
        self.node = BigQueryTable(name="test_node")
        self.node2 = BigQueryTable(name="test_node2")
        self.node3 = BigQueryTable(name="test_node", version=2)

    def teardown_method(self) -> None:
        del self.node
        del self.node2
        del self.node3

    def test_init(self) -> None:
        assert self.node.name == "test_node"
        assert self.node.version == 1
        assert self.node2.name == "test_node2"
        assert self.node2.version == 1
        assert self.node3.name == "test_node"
        assert self.node3.version == 2

    def test_repr(self) -> None:
        assert repr(self.node) == "BigQueryTable(name='test_node', version=1)"
        assert repr(self.node2) == "BigQueryTable(name='test_node2', version=1)"
        assert repr(self.node3) == "BigQueryTable(name='test_node', version=2)"

    def test_hash(self) -> None:
        assert hash(self.node) == hash(("BigQueryTable", "test_node", 1))
        assert hash(self.node2) == hash(("BigQueryTable", "test_node2", 1))
        assert hash(self.node3) == hash(("BigQueryTable", "test_node", 2))


class TestPostgresTable:
    def setup_method(self) -> None:
        self.node = PostgresTable(name="test_node")
        self.node2 = PostgresTable(name="test_node2")
        self.node3 = PostgresTable(name="test_node", version=2)

    def teardown_method(self) -> None:
        del self.node
        del self.node2
        del self.node3

    def test_init(self) -> None:
        assert self.node.name == "test_node"
        assert self.node.version == 1
        assert self.node2.name == "test_node2"
        assert self.node2.version == 1
        assert self.node3.name == "test_node"
        assert self.node3.version == 2

    def test_repr(self) -> None:
        assert repr(self.node) == "PostgresTable(name='test_node', version=1)"
        assert repr(self.node2) == "PostgresTable(name='test_node2', version=1)"
        assert repr(self.node3) == "PostgresTable(name='test_node', version=2)"

    def test_hash(self) -> None:
        assert hash(self.node) == hash(("PostgresTable", "test_node", 1))
        assert hash(self.node2) == hash(("PostgresTable", "test_node2", 1))
        assert hash(self.node3) == hash(("PostgresTable", "test_node", 2))


class TestGoogleCloudStorageObject:
    def setup_method(self) -> None:
        self.node = GoogleCloudStorageObject(name="test_node")
        self.node2 = GoogleCloudStorageObject(name="test_node2")
        self.node3 = GoogleCloudStorageObject(name="test_node", version=2)

    def teardown_method(self) -> None:
        del self.node
        del self.node2
        del self.node3

    def test_init(self) -> None:
        assert self.node.name == "test_node"
        assert self.node.version == 1
        assert self.node2.name == "test_node2"
        assert self.node2.version == 1
        assert self.node3.name == "test_node"
        assert self.node3.version == 2

    def test_repr(self) -> None:
        assert (
            repr(self.node) == "GoogleCloudStorageObject(name='test_node', version=1)"
        )
        assert (
            repr(self.node2) == "GoogleCloudStorageObject(name='test_node2', version=1)"
        )
        assert (
            repr(self.node3) == "GoogleCloudStorageObject(name='test_node', version=2)"
        )

    def test_hash(self) -> None:
        assert hash(self.node) == hash(("GoogleCloudStorageObject", "test_node", 1))
        assert hash(self.node2) == hash(("GoogleCloudStorageObject", "test_node2", 1))
        assert hash(self.node3) == hash(("GoogleCloudStorageObject", "test_node", 2))
