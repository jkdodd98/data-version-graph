import os

from data_version_graph.app import app as flask_app
from data_version_graph.database import create_database
from data_version_graph.graph import Graph


class TestFlaskApp:
    def setup_method(self) -> None:
        # Setup test DB and config
        flask_app.app.config["TESTING"] = True
        flask_app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        flask_app.app.static_folder = "../../tests/app/static"

        self.app = flask_app.app.test_client()
        with flask_app.app.app_context():
            Session = create_database(flask_app.app.config["SQLALCHEMY_DATABASE_URI"])
            session = Session()
            graph = Graph(session=session)
            flask_app.app.config["GRAPH"] = graph

    def teardown_method(self) -> None:
        del self.app

    def test_index(self) -> None:
        response = self.app.get("/")
        assert response.status_code == 200
        assert b"Graph Visualization" in response.data

    def test_refresh_graph(self) -> None:
        response = self.app.post("/refresh-graph")
        assert response.status_code == 302  # Redirect after updating Graph.

        graph_path = os.path.join(flask_app.app.static_folder, "images/graph.png")
        assert os.path.exists(graph_path)

    def test_add_and_remove_node(self) -> None:
        # test invalid add request.
        response = self.app.post("/nodes/add", json={"node_name": "test_node"})
        assert response.status_code == 400  # Invalid request
        assert b"Invalid request" in response.data

        # test valid add request.
        response = self.app.post("/nodes/add", json={"ntype": "Node", "name": "test"})
        assert response.status_code == 200
        assert b"Node added successfully" in response.data

        # test adding existing Node.
        response = self.app.post("/nodes/add", json={"ntype": "Node", "name": "test"})
        assert response.status_code == 200
        assert b"Node added successfully" in response.data

        # test removing invalid Node.
        response = self.app.post("/nodes/remove", json={"node_name": "test_node"})
        assert response.status_code == 400

        # test removing existing Node.
        response = self.app.post(
            "/nodes/remove", json={"ntype": "Node", "name": "test"}
        )
        assert response.status_code == 200
        assert b"Node removed successfully" in response.data

        # test removing non-existent Node.
        response = self.app.post(
            "/nodes/remove", json={"ntype": "PostgresTable", "name": "test_2"}
        )
        assert response.status_code == 200
        assert b"Node removed successfully" in response.data

    def test_add_and_remove_edges(self) -> None:
        # test invalid add request.
        response = self.app.post("/edges/add", json={"source": "test"})
        assert response.status_code == 400
        assert b"Invalid request" in response.data

        # test invalid add request.
        response = self.app.post(
            "/edges/add",
            json={
                "upstream": {"name": "test"},
                "downstream": {"ntype": "test", "name": "test"},
            },
        )
        assert response.status_code == 400
        assert b"Invalid request" in response.data

        # test valid add request.
        response = self.app.post(
            "/edges/add",
            json={
                "upstream": {"ntype": "Node", "name": "test"},
                "downstream": {"ntype": "Node", "name": "test_2"},
            },
        )
        assert response.status_code == 200
        assert b"Edge added successfully" in response.data

        # test adding existing Edge.
        response = self.app.post(
            "/edges/add",
            json={
                "upstream": {"ntype": "Node", "name": "test"},
                "downstream": {"ntype": "Node", "name": "test_2"},
            },
        )
        assert response.status_code == 200
        assert b"Edge added successfully" in response.data

        # test removing invalid Edge.
        response = self.app.post(
            "/edges/remove",
            json={
                "upstream": {"name": "test"},
                "downstream": {"ntype": "test", "name": "test"},
            },
        )
        assert response.status_code == 400
        assert b"Invalid request" in response.data

        # test removing existing Edge.
        response = self.app.post(
            "/edges/remove",
            json={
                "upstream": {"ntype": "Node", "name": "test"},
                "downstream": {"ntype": "Node", "name": "test_2"},
            },
        )
        assert response.status_code == 200
        assert b"Edge removed successfully" in response.data

        # test removing non-existent Edge.
        response = self.app.post(
            "/edges/remove",
            json={
                "upstream": {"ntype": "Node", "name": "test_3"},
                "downstream": {"ntype": "Node", "name": "test_4"},
            },
        )
        assert response.status_code == 200
        assert b"Edge removed successfully" in response.data
