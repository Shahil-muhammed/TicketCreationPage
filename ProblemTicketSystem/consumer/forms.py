# forms.py
from django import forms
from .models import Ticket
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ConsumerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'department', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
