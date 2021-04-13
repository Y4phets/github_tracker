from django import forms


class GithubForm(forms.Form):
    username = forms.CharField(required=True)
