import os
import time
from datetime import datetime
from typing import Union

import requests
from github.retry import retry

__all__ = (
    'GitHubApiSdk',
    'GitHubApiStatusRetryError',
    'GitHubApiQueryLimitException'
)


class GitHubApiStatusRetryError(Exception):
    pass


class GitHubApiQueryLimitException(Exception):
    pass


class GitHubApiSdk:
    PAGE_SIZE = 100
    BACK_OFF_FACTOR = 30
    MAX_REQUEST_RETRY = 5
    STATUS_FORCE_LIST = [413, 429, 500, 502, 503, 504]

    domain = 'https://api.github.com/'
    token = os.getenv('GITHUB_API_TOKEN')
    is_limit_fast_fail = bool(int(os.getenv('GITHUB_QUERY_LIMIT_FAST_FAIL', 0)))

    def get_absolute_path(self, path):
        return f'{self.domain}{path}'

    @retry(exceptions=GitHubApiStatusRetryError, tries=MAX_REQUEST_RETRY, back_off=BACK_OFF_FACTOR)
    def request(self, url: str, options: dict = None) -> (str, list):
        try:
            response = requests.request('get',
                                        url,
                                        params=options)
        except (requests.exceptions.HTTPError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError) as ex:
            raise GitHubApiStatusRetryError(f'Failed to get data from url: {ex}')

        if response.status_code in self.STATUS_FORCE_LIST:
            raise GitHubApiStatusRetryError(f'Response status {response.status_code}')

        if response.status_code == 404:
            return None, None

        if response.status_code == 403:
            reset_time = response.headers['X-RateLimit-Reset']
            limit = response.headers['X-RateLimit-Limit']
            used = response.headers['x-ratelimit-used']
            if self.is_limit_fast_fail:
                raise GitHubApiQueryLimitException(f'Rate limit exceeded, retry request after {reset_time}. '
                                                   f'Limit: {limit}. Used: {used}')

            wait_time = abs(int(reset_time) - datetime.now().timestamp())
            time.sleep(wait_time)
            return self.request(url, options)
        return response.json()

    def get_repos(self, url: str) -> Union[dict, None]:
        data = self.request(self.get_absolute_path(f'users/{url}/repos'), options={'type': 'all'})
        return data

    def get_pull_requests(self, url: str) -> Union[str, list]:
        params = {'per_page': self.PAGE_SIZE,
                  'state': 'all',
                  'sort': 'created'}
        return self.request(self.get_absolute_path(f'repos/{url}/pulls'), options=params)

    def get_count_comments(self, username: str, number: int) -> int:
        return len(requests.get(f'https://api.github.com/repos/{username}/github_api/issues/{number}/comments').json())
