import os
from dataclasses import dataclass
from datetime import datetime
from typing import Self

from .api import MAX_PAGE_SIZE, get_json, get_paginated


@dataclass
class DatasetShort:
    id: int
    modified_at: datetime
    name: str
    description: str
    data_period: str
    unit: str

    @classmethod
    def from_dict(cls, d: dict, in_finnish: bool) -> Self:
        lang = "Fi" if in_finnish else "En"
        return cls(
            d["id"],
            datetime.fromisoformat(d["modifiedAtUtc"]),
            d[f"name{lang}"],
            d[f"description{lang}"],
            d[f"dataPeriod{lang}"],
            d[f"unit{lang}"],
        )

    def __str__(self) -> str:
        s = f"{self.name} [{self.id}]\n"
        s += f"modified at: {self.modified_at}\n"
        s += f"period:      {self.data_period}\n"
        s += f"unit:        {self.unit}\n"
        s += f"description:\n{self.description}\n"
        return s


def get_dataset_shorts(
    search: None | str = None,
    in_finnish: bool = False,
    max_results: None | int = None,
    api_key: str | None = os.environ.get("DATAHUB_APIKEY"),
) -> list[DatasetShort]:
    """query for multiple datasets"""
    params: dict = {"pageSize": max_results or MAX_PAGE_SIZE}
    if search is not None:
        params["search"] = search
    jsons = get_paginated("datasets", params, max_results, api_key)
    return [DatasetShort.from_dict(json, in_finnish) for json in jsons]


@dataclass
class Dataset:
    id: int
    modified_at: datetime
    status: str
    organization: str
    name: str
    description: str
    data_period: str
    unit: str
    update_cadence: str
    key_words: list[str]
    content_groups: list[str]
    available_formats: list[str]

    @classmethod
    def from_dict(cls, d: dict, in_finnish: bool) -> Self:
        lang = "Fi" if in_finnish else "En"
        return cls(
            d["id"],
            datetime.fromisoformat(d["modifiedAtUtc"]),
            d["status"],
            d["organization"],
            d[f"name{lang}"],
            d[f"description{lang}"],
            d[f"dataPeriod{lang}"],
            d[f"unit{lang}"],
            d[f"updateCadence{lang}"],
            d[f"keyWords{lang}"],
            d[f"contentGroups{lang}"],
            d["availableFormats"],
        )

    def __str__(self) -> str:
        s = f"{self.name} [{self.id}]\n"
        s += f"modified at:    {self.modified_at}\n"
        s += f"status:         {self.status}\n"
        s += f"organization:   {self.organization}\n"
        s += f"period:         {self.data_period}\n"
        s += f"unit:           {self.unit}\n"
        s += f"cadence:        {self.update_cadence}\n"
        s += f"keywords:       {self.key_words}\n"
        s += f"content groups: {self.key_words}\n"
        s += f"formats:        {self.available_formats}\n"
        s += f"description:\n{self.description}\n"
        return s


def get_dataset(
    dataset_id: int,
    in_finnish: bool = False,
    api_key: str | None = os.environ.get("DATAHUB_APIKEY"),
) -> Dataset:
    """query for dataset information"""
    json = get_json(f"datasets/{dataset_id}", {}, api_key)
    return Dataset.from_dict(json, in_finnish)
