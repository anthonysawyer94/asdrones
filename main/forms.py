from django import forms
from .models import ProjectInquiry, Review


class ContactForm(forms.ModelForm):
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        label="",
        help_text="Leave this field empty"
    )

    class Meta:
        model = ProjectInquiry
        fields = ['name', 'email', 'phone', 'message']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'service_type', 'rating', 'comment']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5 stars.")
        return rating
