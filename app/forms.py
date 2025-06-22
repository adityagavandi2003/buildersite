from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from app.models import Cutomer,AbstractUser


class UserRegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=16,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+91 \d{10}$',
                message="Phone number must be entered in the format: '+91 9898999898'."
            )
        ]
    )
    class Meta:
        model = User
        fields = ['username','password']

class AgentRegistrationForm(forms.ModelForm):
    class Meta:
        model = AbstractUser
        fields = "__all__"

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Cutomer
        exclude = ['agent', 'created_at']

