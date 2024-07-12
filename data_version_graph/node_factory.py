from data_version_graph.nodes import (
    BigQueryTable,
    GoogleCloudStorageObject,
    Node,
    PostgresTable,
)


class NodeFactory:
    @staticmethod
    def create(node_type: str, **kwargs) -> Node:
        if node_type == "Node":
            return Node(**kwargs)
        elif node_type == "BigQueryTable":
            return BigQueryTable(**kwargs)
        elif node_type == "PostgresTable":
            return PostgresTable(**kwargs)
        elif node_type == "GoogleCloudStorageObject":
            return GoogleCloudStorageObject(**kwargs)
        else:
            raise ValueError(f"Unknown node type: {node_type}")
