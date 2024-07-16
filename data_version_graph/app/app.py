import networkx as nx
from flask import (
    Flask,
    Response,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from data_version_graph.app.validators import Validate
from data_version_graph.database import create_database
from data_version_graph.graph import Graph
from data_version_graph.node_factory import NodeFactory

app = Flask(__name__)


@app.route("/")
def frontpage() -> str:
    return render_template(
        "frontpage.html", url=f"{app.static_folder}/images/graph.png"
    )


# Route to refresh the graph
@app.route("/refresh-graph", methods=["POST"])
def refresh_graph() -> Response:
    graph: Graph = app.config["GRAPH"]
    nx.nx_agraph.to_agraph(graph.graph).draw(
        f"{app.static_folder}/images/graph.png", prog="dot", args="-Nshape=box"
    )

    return redirect(url_for("frontpage"))


@app.route("/nodes/add", methods=["POST"])
def add_node() -> Response:
    data = request.json

    if not Validate.node_request(data):
        return jsonify({"message": "Invalid request.", "status": 400}), 400

    node_type = data.pop("ntype")
    node = NodeFactory.create(node_type, **data)

    graph: Graph = app.config["GRAPH"]
    graph.add_node(node)

    return jsonify({"message": "Node added successfully", "status": 200}), 200


@app.route("/nodes/remove", methods=["POST"])
def remove_node() -> Response:
    data = request.json

    if not Validate.node_request(data):
        return jsonify({"message": "Invalid request.", "status": 400}), 400

    node_type = data.pop("ntype")
    node = NodeFactory.create(node_type, **data)

    graph: Graph = app.config["GRAPH"]
    graph.remove_node(node)

    return jsonify({"message": "Node removed successfully", "status": 200}), 200


@app.route("/edges/add", methods=["POST"])
def add_edge() -> Response:
    data = request.json
    if not Validate.edge_request(data):
        return jsonify({"message": "Invalid request.", "status": 400}), 400

    upstream = data.pop("upstream")
    downstream = data.pop("downstream")

    upstream_node = NodeFactory.create(upstream.pop("ntype"), **upstream)
    downstream_node = NodeFactory.create(downstream.pop("ntype"), **downstream)

    graph: Graph = app.config["GRAPH"]
    graph.add_edge(upstream_node, downstream_node)

    return jsonify({"message": "Edge added successfully", "status": 200}), 200


@app.route("/edges/remove", methods=["POST"])
def remove_edge() -> Response:
    data = request.json
    if not Validate.edge_request(data):
        return jsonify({"message": "Invalid request.", "status": 400}), 400

    upstream = data.pop("upstream")
    downstream = data.pop("downstream")

    upstream_node = NodeFactory.create(upstream.pop("ntype"), **upstream)
    downstream_node = NodeFactory.create(downstream.pop("ntype"), **downstream)

    graph: Graph = app.config["GRAPH"]
    graph.remove_edge(upstream_node, downstream_node)

    return jsonify({"message": "Edge removed successfully", "status": 200}), 200


if __name__ == "__main__":
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///graph.db"  # pragma: no cover
    app.static_folder = "static"  # pragma: no cover
    Session = create_database(app.config["SQLALCHEMY_DATABASE_URI"])  # pragma: no cover
    session = Session()  # pragma: no cover
    graph = Graph(session=session)  # pragma: no cover
    app.config["GRAPH"] = graph  # pragma: no cover

    app.run(debug=True)  # pragma: no cover
