from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.mail import send_mail

from .models import CustomUser, Newsletter

import logging
logger = logging.getLogger(__name__)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        logger.debug(f"Saving user: {user.username}, Email: {user.email}")
        if commit:
            user.is_active = False
            user.save()
            user.generate_confirmation_code()
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {user.confirmation_code}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
        return user

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'birth_date')
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'avatar']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['subject', 'message']

class ConfirmationForm(forms.Form):
    code = forms.CharField(max_length=4, label='Код подтверждения')
