# `fg-cli`

[![build](https://github.com/paasim/fg-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/paasim/fg-cli/actions/workflows/ci.yml)

`fg-cli` - Client for [fingrid open data api](https://developer-data.fingrid.fi/).

## usage

The usage requires API key which can be created in the portal. The following assume that the key is set in the environment variable `DATAHUB_APIKEY`:

```python
from fg_cli import get_dataset, get_dataset_shorts, get_latest_obs, get_obs
from datetime import datetime, UTC

# details for imbalance price dataset
get_dataset(319)

# at most 17 datasets that match the search query price
get_dataset_shorts("price", max_results = 17)

# latest electricity production observation in finland
get_latest_obs(dataset_id = 192)

# electricity consumption observations for the following time period
start_time = datetime(2022, 11, 11, tzinfo = UTC)
end_time = datetime(2022, 11, 12, tzinfo = UTC)
get_obs(dataset_id = 192, start_time = start_time, end_time = end_time)
```
