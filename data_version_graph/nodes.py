from typing import Union

from sqlalchemy import Column


class Node:
    color = "black"

    def __init__(
        self,
        name: Union[str, Column[str]],
        version: Union[int, Column[int]] = 1,
        **properties,
    ) -> None:
        self.name = str(name)
        self.version = int(version)
        self.properties = properties

    @property
    def ntype(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self.name!r}, version={self.version!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        return self.name == other.name and self.version == other.version

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self.name, self.version))


class BigQueryTable(Node):
    color = "#4285F4"


class PostgresTable(Node):
    color = "#0064a5"


class GoogleCloudStorageObject(Node):
    color = "#DB4437"
