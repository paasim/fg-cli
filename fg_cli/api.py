from time import sleep

from requests import Session
from requests.adapters import HTTPAdapter

URL = "https://data.fingrid.fi/api"
TIMEOUT = 20
MAX_PAGE_SIZE = 20000


def _mk_session(api_key: None | str) -> Session:
    if api_key is None:
        raise ValueError("api_key missing")  # noqa: TRY003, EM101
    s = Session()
    s.mount(URL, HTTPAdapter(max_retries=3))
    s.headers.update({"x-api-key": api_key})
    return s


def get_json(
    url_path: str,
    params: dict,
    api_key_or_session: None | str | Session = None,
) -> dict:
    """get query with params to url_path, return resulting json as dict"""
    url = f"{URL}/{url_path}"
    if isinstance(api_key_or_session, Session):
        resp = api_key_or_session.get(url, params=params, timeout=TIMEOUT)
    else:
        with _mk_session(api_key_or_session) as s:
            resp = s.get(url, params=params, timeout=TIMEOUT)

    resp.raise_for_status()
    return resp.json()


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

    with _mk_session(api_key) as session:
        while next_page is not None and (
            max_results is None or len(data) < max_results
        ):
            params["page"] = next_page
            sleep(1)  # sleep between calls
            resp = get_json(url, params, session)
            data += resp["data"]
            next_page = resp["pagination"].get("nextPage")
        return data
