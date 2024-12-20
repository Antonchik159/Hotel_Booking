from django.forms import ModelForm, TextInput, EmailInput, NumberInput, PasswordInput, DateInput, Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client, Booking
from django import forms

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ["client", "room", "start_date", "last_date", "price"]
        widgets = {
            "client": Select(attrs={
                'class': 'form-control form-control-my'
            }),
            "room": Select(attrs={
                'class': 'form-control form-control-my',
                'readonly': 'readonly',
            }),
            "start_date": DateInput(attrs={
                'class': 'form-control form-control-my',
                'type': 'date'
            }),
            "last_date": DateInput(attrs={
                'class': 'form-control form-control-my',
                'type': 'date'
            }),
            "price": TextInput(attrs={
                'class': 'form-control form-control-my',
                'readonly': 'readonly',
            })
        }

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ["fullname", "email", "age", "password"]
        widgets = {
            "fullname": TextInput(attrs={
                'class': 'form-control-my form-control',
                'placeholder': 'Прізвище та імя',
            }),
            "email": EmailInput(attrs={
                'class': 'form-control-my form-control',
                'placeholder': 'Ваша пошта'
            }),
            "age": NumberInput(attrs={
                'class': 'form-control-my form-control',
                'placeholder': 'Ваш вік'
            }),
            "password": PasswordInput(attrs={
                'class': 'form-control-my form-control',
                'placeholder': 'Пароль'
            })
        }

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control-my form-control',
                'placeholder': 'Імя користувача'
            }),
            "email": EmailInput(attrs={
                'class': 'form-control-my form-control',
                'placeholder': 'Ваша пошта'
            }),
            "password1": PasswordInput(attrs={
                'class': 'form-control-my form-control',
                'placeholder': 'Придумайте пароль'
            }),
            "password2": PasswordInput(attrs={
                'class': 'form-control-my form-control',
                'placeholder': 'Повторіть пароль'
            })
        }

class EmailPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Електронна пошта", 
        widget=forms.EmailInput(attrs={
            'class': 'form-control-my form-control',
            'placeholder': 'Ваша пошта'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control-my form-control',
            'placeholder': 'Пароль'
        }),
        label="Пароль"
    )

class BookingApprovalForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['approved']
        widgets = {
            'approved': forms.Select(attrs={'style': 'font-size: 15px;'}, choices=[(True, 'Підтверджено'), (False, 'Відхилено')])
        }