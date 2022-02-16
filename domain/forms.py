from urllib.parse import urlparse

from django import forms
from domain.models import Domain


class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ("name",)

    def clean(self):
        cleaned_data = super(DomainForm, self).clean()
        parsed_url = urlparse(cleaned_data['name'])
        cleaned_data['name'] = parsed_url.scheme + "://" + parsed_url.netloc
        return cleaned_data
