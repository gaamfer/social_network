from django import forms
from network.models import Profile

class ProfileForm(forms.Form):
    class Meta:
        model = Profile
        exclude = ["user", "username", "following"]
        