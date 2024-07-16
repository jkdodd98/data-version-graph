from typing import Union

from sqlalchemy import Column

from data_version_graph.nodes import (
    BigQueryTable,
    GoogleCloudStorageObject,
    Node,
    PostgresTable,
)


class NodeFactory:
    @staticmethod
    def create(
        node_type: Union[str, Column[str]],
        *,
        name: Union[str, Column[str]],
        version: Union[int, Column[int]] = 1,
    ) -> Node:
        if node_type == "Node":
            return Node(name, version=version)
        elif node_type == "BigQueryTable":
            return BigQueryTable(name, version=version)
        elif node_type == "PostgresTable":
            return PostgresTable(name, version=version)
        elif node_type == "GoogleCloudStorageObject":
            return GoogleCloudStorageObject(name, version=version)
        else:
            raise ValueError(f"Unknown node type: {node_type}")
