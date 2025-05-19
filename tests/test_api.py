import time
from datetime import UTC, datetime, timedelta

import pytest
from requests import HTTPError

from fg_cli import get_dataset, get_dataset_shorts, get_health, get_latest_obs, get_obs


@pytest.fixture(autouse=True)
def slow_down_tests():
    """yield for test, then wait for 7 seconds before next test for api rate limit"""
    yield
    time.sleep(7)


def test_missing_apikey():
    """No apikey results in an error"""
    with pytest.raises(ValueError):
        get_health(None)


def test_invalid_apikey():
    """No apikey results in an error"""
    with pytest.raises(HTTPError):
        get_health("invalid_apikey")


def test_health():
    """get_healths retusn that the app works"""
    health = get_health()
    assert health.app == "OK"


def test_dataset():
    """get_dataset works for series 319 (imbalance price)"""
    dataset_id = 319
    dataset = get_dataset(dataset_id)
    assert dataset.id == dataset_id
    # in practice the dataset might change
    assert dataset.name == "Imbalance price"
    assert dataset.unit == "1 €/MWh"
    assert dataset.data_period == "15 min"
    assert "json" in dataset.available_formats


def test_dataset_in_finnish():
    """get_dataset works in finnish"""
    dataset_id = 319
    dataset = get_dataset(dataset_id, in_finnish=True)
    assert dataset.id == dataset_id
    # in practice the dataset might change
    assert dataset.name == "Tasepoikkeaman hinta"
    assert dataset.unit == "1 €/MWh"
    assert dataset.data_period == "15 min"
    assert "json" in dataset.available_formats


def test_dataset_shorts_with_query():
    """query with wind power returns 'max_results' number of results"""
    max_results = 5
    datasets = get_dataset_shorts("wind power", max_results=max_results)
    assert len(datasets) == max_results
    assert "wind power" in datasets[0].name.lower()


def test_dataset_shorts_with_query_in_finnish():
    """query with wind power in finnish returns more than 5 results with word 'tuuli'"""
    datasets = get_dataset_shorts("wind power", in_finnish=True)
    more_than_when_limiting_to_5 = 5
    assert len(datasets) > more_than_when_limiting_to_5
    assert "tuuli" in datasets[0].name.lower()


def test_get_latest_obs():
    """latest observation is less than 1 hour ago"""
    dataset_id = 74
    hour_ago = datetime.now(UTC) - timedelta(hours=1)
    obs = get_latest_obs(dataset_id)
    assert obs.dataset_id == dataset_id
    assert hour_ago < obs.start_time


def test_get_obs():
    """get_obs returns data from 2014"""
    dataset_id = 192
    max_results = 27
    obs = get_obs(dataset_id, max_results=max_results)
    # in practice this might change
    assert len(obs) == max_results
    assert obs[0].start_time == datetime(2014, 1, 1, tzinfo=UTC)
    assert obs[0].value == 7676


def test_get_obs_start_time():
    """start_time works for get_obs"""
    dataset_id = 192
    max_results = 3
    dt = datetime(2024, 11, 11, 11, 12, tzinfo=UTC)
    obs = get_obs(dataset_id, start_time=dt, max_results=max_results)
    # in practice this might change
    assert len(obs) == max_results
    assert obs[0].start_time == dt
    assert obs[0].value == 9144.5
