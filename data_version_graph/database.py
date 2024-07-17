from typing import Any

from sqlalchemy import JSON, Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base: Any = declarative_base()


class NodeModel(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True)
    ntype = Column(String, nullable=False)
    name = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    kwargs = Column(JSON, nullable=True)


class EdgeModel(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True)
    from_node_id = Column(Integer, ForeignKey("nodes.id"), nullable=False)
    to_node_id = Column(Integer, ForeignKey("nodes.id"), nullable=False)

    from_node = relationship("NodeModel", foreign_keys=[from_node_id])
    to_node = relationship("NodeModel", foreign_keys=[to_node_id])


def create_database(database_url: str) -> sessionmaker:
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)

    return sessionmaker(bind=engine)
