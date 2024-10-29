from django import forms
from network.models import Profile

class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=True)

    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'birth_date', 'sex']
        