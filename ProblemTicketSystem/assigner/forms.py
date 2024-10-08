from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

class AssignerSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

    def clean_username(self):
        username= self.cleaned_data.get('username')
        return f"{username}_localstaff"
    
class AssignerLoginForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Append "_localstaff" to the username
            return f"{username}_localstaff"
        raise forms.ValidationError("Username is required.")