from sqlalchemy import JSON, Integer, String, inspect
from sqlalchemy.orm import sessionmaker

from data_version_graph.database import EdgeModel, NodeModel, create_database


def test_create_database():
    db_url = "sqlite:///:memory:"
    Session = create_database(db_url)

    assert isinstance(Session, sessionmaker)
    assert Session.kw["bind"].url.database == ":memory:"

    session = Session()

    # Check that the tables were created
    inspector = inspect(session.bind)
    assert "nodes" in inspector.get_table_names()
    assert "edges" in inspector.get_table_names()

    # verify that the tables have the expected columns
    columns = inspector.get_columns("nodes")
    assert len(columns) == 5
    assert columns[0]["name"] == "id"
    assert isinstance(columns[0]["type"], Integer)
    assert columns[1]["name"] == "ntype"
    assert isinstance(columns[1]["type"], String)
    assert columns[2]["name"] == "name"
    assert isinstance(columns[2]["type"], String)
    assert columns[3]["name"] == "version"
    assert isinstance(columns[3]["type"], Integer)
    assert columns[4]["name"] == "properties"
    assert isinstance(columns[4]["type"], JSON)

    columns = inspector.get_columns("edges")
    assert len(columns) == 3
    assert columns[0]["name"] == "id"
    assert columns[1]["name"] == "from_node_id"
    assert columns[2]["name"] == "to_node_id"

    # verify that the tables are empty
    nodes = session.query(NodeModel).all()
    assert nodes == []
    edges = session.query(EdgeModel).all()
    assert edges == []
