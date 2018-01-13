from django import forms


class AnswerForm(forms.Form):
    ans = forms.CharField(label='Answer here...', max_length=1000)
