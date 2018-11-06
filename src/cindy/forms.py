from django import forms


class SubmissionForm(forms.Form):
    url = forms.URLField(required=True)
