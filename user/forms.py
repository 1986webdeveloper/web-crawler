"""
	import needed things
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    """
			NewUserForm
	"""
    email = forms.EmailField(required=True)

    class Meta:
        """
			User model data
        """
    model = User
    fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        """
			save method
		"""
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
