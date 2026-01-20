from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


class CustomSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)

        # use email as username internally
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user
    
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmailLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Email address"
        })
    )


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'
