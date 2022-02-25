"""
    below urlparse for getting name
"""
from urllib.parse import urlparse
from django import forms
from domain.models import Domain


class DomainForm(forms.ModelForm):
    """
        Form Validation
    """
    class Meta:
        """
            Getting Model Details
        """
        model = Domain
        fields = ("name",)

        def __str__(self):
            return self.__class__.__name__

    def clean(self):
        """
            Clean Method For Form Submit
        """
        cleaned_data = super(DomainForm, self).clean()
        parsed_url = urlparse(cleaned_data.get('name'))
        cleaned_data['name'] = f"{parsed_url.scheme}://{parsed_url.netloc}"
