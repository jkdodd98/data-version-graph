import uuid


class Node:
    def __init__(self, name: str, *, version: int = 1) -> None:
        self.pid = uuid.uuid4()
        self.name = name
        self.version = version

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self.name!r}, version={self.version!r})"
        )

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self.name, self.version))


class BigQueryTable(Node):
    ...


class PostgresTable(Node):
    ...


class GoogleCloudStorageObject(Node):
    ...
