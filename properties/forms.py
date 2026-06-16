from django import forms
from .models import ConsultationLead
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ConsultationForm(forms.ModelForm):

    class Meta:

        model = ConsultationLead

        fields = [

            "customer_name",

            "email",

            "phone",

            "budget",

            "requirements",

        ]

class CustomerRegistrationForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:

        model = User

        fields = (
            'username',
            'email',
            'full_name',
            'phone',
            'city',
            'password1',
            'password2'
        )

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )

        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )