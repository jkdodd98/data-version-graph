from data_version_graph.app.validators import Validate


class TestValidators:
    def test_node_request(self):
        data = {"ntype": "test", "name": "test"}
        assert Validate.node_request(data) is True

        data = {"ntype": "test", "name": "test", "version": 1}
        assert Validate.node_request(data) is True

        data = {"ntype": "test", "name": "test", "version": 1, "extra": "extra"}
        assert Validate.node_request(data) is True

    def test_node_request_invalid(self):
        data = {"name": "test"}
        assert Validate.node_request(data) is False

        data = {"ntype": "test"}
        assert Validate.node_request(data) is False

        data = {"ntype": "test", "version": 1}
        assert Validate.node_request(data) is False

        data = None
        assert Validate.node_request(data) is False

    def test_edge_request(self):
        data = {
            "upstream": {"ntype": "test", "name": "test"},
            "downstream": {"ntype": "test", "name": "test"},
        }
        assert Validate.edge_request(data) is True

        data = {
            "upstream": {"ntype": "test", "name": "test", "version": 1},
            "downstream": {"ntype": "test", "name": "test_2", "version": 1},
        }
        assert Validate.edge_request(data) is True

        data = {
            "upstream": {"ntype": "test", "name": "test"},
            "downstream": {"ntype": "test", "name": "test_2", "version": 2},
        }
        assert Validate.edge_request(data) is True

    def test_edge_request_invalid(self):
        data = {
            "upstream": {"name": "test"},
            "downstream": {"ntype": "test", "name": "test"},
        }
        assert Validate.edge_request(data) is False

        data = {
            "source": {"ntype": "test", "name": "test"},
            "target": {"ntype": "test", "name": "test_2"},
        }
        assert Validate.edge_request(data) is False

        data = {
            "upstream": {"ntype": "test", "name": "test"},
        }
        assert Validate.edge_request(data) is False

        data = {
            "downstream": {"ntype": "test", "name": "test", "version": 1},
        }
        assert Validate.edge_request(data) is False

        data = None
        assert Validate.edge_request(data) is False
