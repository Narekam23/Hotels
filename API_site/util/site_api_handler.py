from typing import Dict

import requests
import backoff


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=8,
                      jitter=None)
def _make_response(method: str, url: str, headers: Dict, payload: Dict,
                   timeout: int, success: object = 200) -> object:
    """Основная функция для запросов."""
    if method == "GET":
        response = requests.get(
            url,
            headers=headers,
            params=payload,
            timeout=timeout
        )

        status_code = response.status_code

        if status_code == success:
            return response

        return status_code

    elif method == "POST":
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=timeout
        )

        status_code = response.status_code

        if status_code == success:
            return response

        return status_code


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=8,
                      jitter=None)
def _locations_search(url: str, headers: Dict, payload: Dict, timeout: int,
                      func=_make_response) -> object:
    method = "GET"
    url = "{url}/locations/v3/search".format(url=url)
    response = func(method, url, headers=headers,
                    payload=payload, timeout=timeout)

    return response


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=8,
                      jitter=None)
def _properties_list(url: str, headers: Dict, payload: Dict, timeout: int,
                     func=_make_response) -> object:
    method = "POST"
    url = "{url}/properties/v2/list".format(url=url)
    response = func(method, url, payload=payload, headers=headers, timeout=timeout)

    return response


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=8,
                      jitter=None)
def _properties_detail(url: str, headers: Dict, payload: Dict, timeout: int,
                       func=_make_response) -> object:
    method = "POST"
    url = "{url}/properties/v2/detail".format(url=url)
    response = func(method, url, payload=payload, headers=headers, timeout=timeout)

    return response


class SiteApiInterface():
    @staticmethod
    def locations_search():
        return _locations_search

    @staticmethod
    def properties_list():
        return _properties_list

    @staticmethod
    def properties_detail():
        return _properties_detail


if __name__ == '__main__':
    _make_response()
    _locations_search()
    _properties_list()
    _properties_detail()

    SiteApiInterface()
