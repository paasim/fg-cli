from time import sleep

from requests import get
from requests.exceptions import Timeout

URL = "https://data.fingrid.fi/api"
TIMEOUT = 20
MAX_PAGE_SIZE = 20000


def get_json(
    url_path: str, params: dict, api_key: None | str, max_retries: int = 2
) -> dict:
    """get query with params to url_path, return resulting json as dict"""
    if api_key is None:
        raise ValueError("api_key missing")  # noqa: TRY003, EM101
    headers = {"x-api-key": api_key}
    url = f"{URL}/{url_path}"
    tries = 0
    while True:
        try:
            resp = get(url, params=params, headers=headers, timeout=TIMEOUT)
            resp.raise_for_status()
            return resp.json()
        except Timeout:
            if tries >= max_retries:
                raise
            sleep(1)
            tries += 1


def get_paginated(
    url: str,
    params: dict,
    max_results: None | int,
    api_key: None | str,
) -> list[dict]:
    """query a paginated api
    return resulting elements (json with list of object) as list of dicts"""
    resp = get_json(url, params, api_key)
    data = resp["data"]
    next_page = resp["pagination"].get("nextPage")

    while next_page is not None and (max_results is None or len(data) < max_results):
        params["page"] = next_page
        sleep(1)  # sleep between calls
        resp = get_json(url, params, api_key)
        data += resp["data"]
        next_page = resp["pagination"].get("nextPage")
    return data
