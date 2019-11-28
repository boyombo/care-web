from django import forms


class RejectForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea)
