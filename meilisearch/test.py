from __future__ import annotations

from datetime import datetime
from time import sleep
from typing import Any
from urllib import parse

from meilisearch._httprequests import HttpRequests
from meilisearch.config import Config
from meilisearch.errors import MeiliSearchTimeoutError


def get_tasks(config: Config, parameters: dict[str, Any] | None = None) -> dict[str, list[dict[str, Any]]]:
    """Get all tasks.

    Parameters
    ----------
    config:
        Config object containing permission and location of Meilisearch.
    parameters (optional):
        parameters accepted by the get tasks route: https://docs.meilisearch.com/reference/api/tasks.html#get-all-tasks.
        `indexUid` should be set as a List.

    Returns
    -------
    task:
        Dictionary with limit, from, next and results containing a list of all enqueued, processing, succeeded or failed tasks.

    Raises
    ------
    MeiliSearchApiError
        An error containing details about why Meilisearch can't process your request. Meilisearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
    """
    http = HttpRequests(config)
    if parameters is None:
        parameters = {}
    for param in parameters:
        if isinstance(parameters[param], list):
            parameters[param] = ",".join(parameters[param])
    return http.get(
        f"{config.paths.task}?{parse.urlencode(parameters)}"
    )