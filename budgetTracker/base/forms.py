from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class CustomAuthenticationForm(forms.Form):
    username = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        User = get_user_model() 
        try:
            user = User.objects.get(email=username)  
        except User.DoesNotExist:
            raise forms.ValidationError("This email address is not registered.")
        return user

class CustomUserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required fields
    plus a repeated password field for confirmation.
    """
    password1 = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
    )
    password2 = forms.CharField(
        label="Confirm Password", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
    )
    email = forms.EmailField(
        label="Email", 
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    name = forms.CharField(
        label="Username", 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    phone=forms.CharField(
        label="phone",
        widget= forms.TextInput(attrs={'placeholder': 'Enter your Phone'})
    )
    class Meta:
        model = User
        fields = ["name", "email", "phone"]

    def clean_email(self):
        # Ensure email is unique
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
       
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  
        if commit:
            user.save()
        return user
class CustomUserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all user fields but displays the password
    as a read-only hash.
    """
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text="Passwords are stored securely and cannot be viewed. "
                  "You can reset the password using <a href='../password/'>this form</a>.",
    )

    class Meta:
        model = User
        fields = ["name", "email", "phone", "password", "is_active", "is_admin"]

    def clean_password(self):
        
        return self.initial["password"]
from .models import EMI

class EMIForm(forms.ModelForm):
    class Meta:
        model = EMI
        fields = ['amount', 'start_date', 'end_date', 'frequency', 'description', 'next_payment_date']