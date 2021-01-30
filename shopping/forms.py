from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'first_name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'last_name'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mobile'}))
    profile = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'profile'}))
    alternate_mobil_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'alternate_mobil_number'}))
  
    class Meta:
        model = Profile
        fields = "__all__"