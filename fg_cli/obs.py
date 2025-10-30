import os
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from typing import Self

from .api import MAX_PAGE_SIZE, get_json, get_paginated


@dataclass
class Obs:
    dataset_id: int
    start_time: datetime
    end_time: datetime
    value: float

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        return cls(
            d["datasetId"],
            datetime.fromisoformat(d["startTime"]),
            datetime.fromisoformat(d["endTime"]),
            d["value"],
        )

    def __str__(self) -> str:
        s = f"{self.start_time}--{self.end_time}\n"
        s += f"{self.value}\n"
        return s

    def __iter__(self) -> Iterator[int | datetime | float]:
        yield self.dataset_id
        yield self.start_time
        yield self.end_time
        yield self.value


def get_obs(
    dataset_id: int,
    start_time: None | datetime = None,
    end_time: None | datetime = None,
    max_results: None | int = None,
    api_key: str | None = os.environ.get("DATAHUB_APIKEY"),
) -> list[Obs]:
    """get multiple observations from a dataset"""
    path = f"datasets/{dataset_id}/data"
    params = {
        "pageSize": max_results or MAX_PAGE_SIZE,
        "sortOrder": "asc",
    }
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    jsons = get_paginated(path, params, max_results, api_key)
    return [Obs.from_dict(json) for json in jsons]


def get_latest_obs(
    dataset_id: int,
    api_key: str | None = os.environ.get("DATAHUB_APIKEY"),
) -> Obs:
    """get latest observation from a dataset"""
    path = f"datasets/{dataset_id}/data/latest"
    return Obs.from_dict(get_json(path, {}, api_key))
