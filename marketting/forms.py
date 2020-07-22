from django import forms

from .models import MarkettingPreference


class MarkettingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Receive Marketing Email?', required=False)
    class Meta:
        model = MarkettingPreference
        fields = [
            'subscribed'
        ]
