from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

  
class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form to include email field and additional validations.
    """
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        """
        Ensure the email is unique.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
