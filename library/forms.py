from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.fields import CharField, DateField, EmailField
from django import forms
from users.models import User


class CreateUserForm(UserCreationForm):
    full_name = CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Jon Doe'})
    )
    personal_number = CharField(
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={'type': 'number', 'class': 'form-control', 'placeholder': '01028279966'})
    )
    birth_date = DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    email = EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'user@gmail.com'}),
        max_length=64,
    )
    password1 = CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'})
    )

    class Meta:
        model = User
        fields = ('full_name', 'personal_number', 'birth_date', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'user@gmail.com'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Email"
        self.fields['username'].widget.attrs['placeholder'] = 'user@gmail.com'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
