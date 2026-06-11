from django import forms

from .models import Consultation


class BookingForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ["name", "email", "phone", "notes"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your full name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "you@example.com"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "(555) 123-4567"}
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Any topics you'd like to discuss?",
                    "rows": 3,
                }
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        return phone.strip()
