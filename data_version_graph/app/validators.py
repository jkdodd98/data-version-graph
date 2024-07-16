from typing import Optional


class Validate:
    @staticmethod
    def node_request(data: Optional[dict]) -> bool:
        if data is None:
            return False
        return all(key in data for key in ["ntype", "name"])

    @staticmethod
    def edge_request(data: Optional[dict]) -> bool:
        if data is None:
            return False
        return all(key in data for key in ["upstream", "downstream"]) and all(
            Validate.node_request(data[key]) for key in data
        )
