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
        fields = ['title', 'department', 'description', 'user']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'user': forms.HiddenInput()  # Hidden field for user
        }

    def __init__(self, *args, **kwargs):
        # Get the user from the keyword arguments
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # Ensure the user field is set before saving
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance