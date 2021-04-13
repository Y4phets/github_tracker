import requests
from django.http import JsonResponse
from django.shortcuts import render

from github.forms import GithubForm

from github.controller import ReportController
from github.sdk import GitHubApiSdk

token = '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'
some_list = []


def get_cnt_comments(username, number):
    return len(requests.get(f'https://api.github.com/repos/{username}/github_api/issues/{number}/comments').json())


def main(request):
    some_list = []
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    form = GithubForm(request.POST or None)

    if request.POST:
        if not form.is_valid():
            return JsonResponse(
                {'status': 'error', 'data': form.errors},
            )
        data = request.POST
        username = data.get("username")
        sdk = GitHubApiSdk()
        controller = ReportController(sdk=sdk,
                                      username=username)
        some_list = controller.make()

    return render(request, 'base.html', {"data": some_list})
