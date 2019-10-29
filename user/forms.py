from django import forms
from .models import CustomUser


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'pass'
    }))
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'pass'
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'email')
