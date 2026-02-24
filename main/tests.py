from django.test import TestCase
from django.urls import reverse

from .models import ProjectInquiry


class ContactFormTest(TestCase):
    def test_valid_form_submission(self):
        """Test that valid form data creates an inquiry."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Test message'
        }
        response = self.client.post(reverse('main:home'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ProjectInquiry.objects.filter(email='john@example.com').exists())

    def test_invalid_form_submission(self):
        """Test that invalid form data fails validation."""
        data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'message': ''
        }
        response = self.client.post(reverse('main:home'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ProjectInquiry.objects.exists())

    def test_get_request(self):
        """Test that GET request returns the form."""
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)

    def test_inquiry_has_ip_address(self):
        """Test that inquiry captures IP address."""
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'Test'
        }
        self.client.post(reverse('main:home'), data)
        inquiry = ProjectInquiry.objects.first()
        self.assertIsNotNone(inquiry.ip_address)


class ProjectInquiryModelTest(TestCase):
    def test_str_representation(self):
        """Test the string representation of the model."""
        inquiry = ProjectInquiry(
            name="Test User",
            email="test@example.com",
            message="Test message"
        )
        self.assertEqual(str(inquiry), "Test User - test@example.com")
