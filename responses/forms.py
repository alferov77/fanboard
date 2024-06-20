from django import forms
from .models import Responses

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Responses
        fields = ['text']
