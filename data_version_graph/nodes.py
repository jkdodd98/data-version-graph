class Node:
    color = "black"

    def __init__(self, name: str, *, version: int = 1) -> None:
        self.name = name
        self.version = version

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
    color = "blue"


class PostgresTable(Node):
    color = "red"


class GoogleCloudStorageObject(Node):
    color = "green"
