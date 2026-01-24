from django import forms
from .models import ProjectInquiry


class ContactForm(forms.ModelForm):
    class Meta:
        model = ProjectInquiry
        fields = ['name', 'email', 'message']
