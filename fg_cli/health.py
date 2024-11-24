import os
from dataclasses import dataclass
from typing import Self

from .api import get_json


@dataclass
class Health:
    app: str
    database: str
    network: str

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        app = d["app"]["status"]
        database = d["database"]["status"]
        network = d["network"]["status"]
        return cls(app, database, network)

    def __str__(self) -> str:
        s = "Health\n"
        s += f"app:      {self.app}\n"
        s += f"database: {self.database}\n"
        s += f"network:  {self.network}\n"
        return s


def get_health(api_key: str | None = os.environ.get("DATAHUB_APIKEY")) -> Health:
    """query for service health"""
    return Health.from_dict(get_json("health", {}, api_key))
