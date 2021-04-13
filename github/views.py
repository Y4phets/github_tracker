import requests
from django.http import JsonResponse
from django.shortcuts import render

from github.forms import GithubForm

from github.controller import ReportController
from github.sdk import GitHubApiSdk


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
        username = data.get('username')
        sdk = GitHubApiSdk()
        controller = ReportController(sdk=sdk,
                                      username=username)
        some_list = controller.make()

    return render(request, 'base.html', {'data': some_list})
