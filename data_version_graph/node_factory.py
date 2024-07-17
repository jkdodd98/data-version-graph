from typing import Any, Optional, Union

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
        properties: Optional[dict[str, Any]] = None,
    ) -> Node:
        properties = {} if properties is None else properties

        if node_type == "Node":
            return Node(name, version=version)
        elif node_type == "BigQueryTable":
            return BigQueryTable(name, version=version, properties=properties)
        elif node_type == "PostgresTable":
            return PostgresTable(name, version=version, properties=properties)
        elif node_type == "GoogleCloudStorageObject":
            return GoogleCloudStorageObject(
                name, version=version, properties=properties
            )
        else:
            raise ValueError(f"Unknown node type: {node_type}")
