from django.test import TestCase
from django.urls import reverse
from django.core import mail

from main.models import ProjectInquiry, Review
from main.forms import ContactForm, ReviewForm


class ContactFormTest(TestCase):
    def test_valid_form_submission(self):
        """Test that valid form data creates an inquiry."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '555-1234',
            'message': 'Test message',
        }
        response = self.client.post(reverse('main:home'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ProjectInquiry.objects.filter(email='john@example.com').exists())

    def test_valid_form_with_ip_capture(self):
        """Test that IP address is captured from request."""
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'message': 'Hello world',
        }
        response = self.client.post(reverse('main:home'), data, REMOTE_ADDR='192.168.1.1')
        inquiry = ProjectInquiry.objects.get(email='jane@example.com')
        self.assertEqual(inquiry.ip_address, '192.168.1.1')

    def test_valid_form_with_x_forwarded_for(self):
        """Test that X-Forwarded-For header is handled correctly."""
        data = {
            'name': 'Alice Smith',
            'email': 'alice@example.com',
            'message': 'Testing',
        }
        response = self.client.post(
            reverse('main:home'),
            data,
            HTTP_X_FORWARDED_FOR='10.0.0.1, 10.0.0.2'
        )
        inquiry = ProjectInquiry.objects.get(email='alice@example.com')
        self.assertEqual(inquiry.ip_address, '10.0.0.1')

    def test_invalid_form_submission(self):
        """Test that invalid form data is rejected."""
        data = {
            'name': 'Bob',
            'email': 'not-an-email',
            'message': '',
        }
        response = self.client.post(reverse('main:home'), data)
        self.assertFalse(ProjectInquiry.objects.filter(name='Bob').exists())

    def test_honeypot_blocks_submission(self):
        """Test that honeypot field blocks bot submissions."""
        data = {
            'name': 'Bot',
            'email': 'bot@example.com',
            'message': 'Spam',
            'website': 'http://spam.com',
        }
        response = self.client.post(reverse('main:home'), data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ProjectInquiry.objects.filter(email='bot@example.com').exists())


class ReviewFormTest(TestCase):
    def test_valid_review_submission(self):
        """Test that valid review is created."""
        data = {
            'name': 'Happy Customer',
            'service_type': 'aerial',
            'rating': 5,
            'comment': 'Great service!',
        }
        response = self.client.post(reverse('main:leave_review'), data)
        self.assertEqual(Review.objects.count(), 1)
        self.assertFalse(Review.objects.first().is_approved)

    def test_invalid_rating(self):
        """Test that rating outside 1-5 is rejected."""
        data = {
            'name': 'Unhappy',
            'service_type': 'survey',
            'rating': 6,
            'comment': 'Bad',
        }
        response = self.client.post(reverse('main:leave_review'), data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_approved_reviews_visible(self):
        """Test that only approved reviews are shown."""
        Review.objects.create(
            name='Approved',
            service_type='aerial',
            rating=5,
            comment='Great',
            is_approved=True
        )
        Review.objects.create(
            name='Pending',
            service_type='survey',
            rating=4,
            comment='Good',
            is_approved=False
        )
        response = self.client.get(reverse('main:reviews'))
        self.assertContains(response, 'Approved')
        self.assertNotContains(response, 'Pending')
