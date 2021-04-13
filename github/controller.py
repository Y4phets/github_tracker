import sys
from dataclasses import dataclass
from typing import Union

from github.sdk import GitHubApiSdk

__all__ = (
    'ReportController'
)


@dataclass
class ReportController:
    sdk: GitHubApiSdk
    username: str

    def get_repos_meta(self) -> Union[dict, None]:
        repos = self.sdk.get_repos(self.username)
        if repos is None:
            return
        return repos

    def make(self) -> None:
        data = []
        repos = self.get_repos_meta()
        if repos is None:
            sys.stdout.write(f'Repository for {self.username} not found!')
            return

        for repo in repos:
            full_name = repo['full_name']
            owner = repo['repo']['login']
            prs = self.sdk.get_pull_requests(repo['full_name'])
            list_pr = [pr for pr in prs if pr['user']['login'] == self.username]
            sys.stdout.write(f'Open pull requests: \n')
            if list_pr:
                data.append({'name_project': full_name,
                             'url': repo['url'],
                             'stargazers_count': repo['stargazers_count'],
                             'open': [
                                 {'url': pr['url'],
                                  'cnt_comments': self.sdk.get_count_comments(owner, pr['number'])}
                                 for pr in
                                 list_pr if
                                 pr['state'] == 'open'],
                             'close': [
                                 {'url': pr['url'],
                                  'cnt_comments': self.sdk.get_count_comments(owner, pr['number'])}
                                 for pr in
                                 list_pr
                                 if pr['state'] == 'closed']})
        return data
