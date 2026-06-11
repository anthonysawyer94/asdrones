import datetime
from datetime import date, timedelta

from django.contrib.messages import get_messages
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .forms import BookingForm
from .models import Availability, Consultation


def _get_available_slots(target_date):
    """Replicate the helper from views for testing."""
    weekday = target_date.weekday()
    avail_blocks = Availability.objects.filter(day_of_week=weekday, is_active=True)
    if not avail_blocks:
        return []
    booked = Consultation.objects.filter(
        date=target_date, status__in=["pending", "approved"]
    ).values_list("time", flat=True)
    slots = []
    for block in avail_blocks:
        current = datetime.datetime.combine(target_date, block.start_time)
        end = datetime.datetime.combine(target_date, block.end_time)
        while current + timedelta(minutes=30) <= end:
            slot_time = current.time()
            if slot_time not in booked:
                slots.append(slot_time)
            current += timedelta(minutes=30)
    return slots


class AvailabilityModelTest(TestCase):
    def test_str_representation(self):
        avail = Availability.objects.create(
            day_of_week=0, start_time="09:00", end_time="17:00"
        )
        result = str(avail)
        self.assertIn("Monday", result)
        self.assertIn("09", result)

    def test_verbose_name_plural(self):
        self.assertEqual(Availability._meta.verbose_name_plural, "Availability")


class ConsultationModelTest(TestCase):
    def test_str_representation(self):
        consultation = Consultation.objects.create(
            name="John Doe",
            email="john@example.com",
            date=date.today() + timedelta(days=1),
            time="10:00",
        )
        result = str(consultation)
        self.assertIn("John Doe", result)

    def test_default_status_is_pending(self):
        consultation = Consultation.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            date=date.today() + timedelta(days=1),
            time="11:00",
        )
        self.assertEqual(consultation.status, "pending")


@override_settings(SECURE_SSL_REDIRECT=False)
class BookingViewTest(TestCase):
    def setUp(self):
        Availability.objects.create(
            day_of_week=0, start_time="09:00", end_time="12:00", is_active=True
        )

    def test_booking_page_renders(self):
        response = self.client.get(reverse("fora:book"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fora/book.html")

    def test_available_dates_shown_for_monday(self):
        response = self.client.get(reverse("fora:book"))
        self.assertIn("available_dates", response.context)
        self.assertTrue(len(response.context["available_dates"]) > 0)

    def test_get_slots_for_monday(self):
        today = timezone.localdate()
        days_ahead = (0 - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        next_monday = today + timedelta(days=days_ahead)
        response = self.client.get(
            reverse("fora:book"), {"date": next_monday.isoformat()}
        )
        self.assertIn("available_slots", response.context)
        self.assertTrue(len(response.context["available_slots"]) > 0)

    def test_booking_min_one_day_advance(self):
        today = timezone.localdate()
        response = self.client.post(
            reverse("fora:book"),
            {
                "date": today.isoformat(),
                "time": "10:00",
                "name": "Test User",
                "email": "test@example.com",
            },
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("at least one day in advance" in str(m) for m in messages))

    def test_successful_booking(self):
        tomorrow = timezone.localdate() + timedelta(days=1)
        while tomorrow.weekday() != 0:
            tomorrow += timedelta(days=1)

        response = self.client.post(
            reverse("fora:book"),
            {
                "date": tomorrow.isoformat(),
                "time": "10:00",
                "name": "Alice Smith",
                "email": "alice@example.com",
                "phone": "555-0100",
                "notes": "Looking forward!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Consultation.objects.filter(email="alice@example.com").exists())

    def test_duplicate_slot_rejected(self):
        tomorrow = timezone.localdate() + timedelta(days=1)
        while tomorrow.weekday() != 0:
            tomorrow += timedelta(days=1)

        Consultation.objects.create(
            name="First",
            email="first@example.com",
            date=tomorrow,
            time="10:00",
            status="pending",
        )

        response = self.client.post(
            reverse("fora:book"),
            {
                "date": tomorrow.isoformat(),
                "time": "10:00",
                "name": "Second",
                "email": "second@example.com",
            },
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("no longer available" in str(m) for m in messages))


@override_settings(SECURE_SSL_REDIRECT=False)
class ConfirmationViewTest(TestCase):
    def test_confirmation_page(self):
        consultation = Consultation.objects.create(
            name="Test User",
            email="test@example.com",
            date=date.today() + timedelta(days=1),
            time="14:00",
        )
        response = self.client.get(reverse("fora:confirmation", args=[consultation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fora/confirmation.html")
        self.assertContains(response, "Test User")


class HelperFunctionTest(TestCase):
    def test_get_available_slots_no_availability(self):
        slots = _get_available_slots(date.today() + timedelta(days=1))
        self.assertEqual(slots, [])

    def test_get_available_slots_with_availability(self):
        Availability.objects.create(
            day_of_week=0, start_time="09:00", end_time="10:00", is_active=True
        )
        next_monday = date.today() + timedelta(
            days=(0 - date.today().weekday()) % 7 or 7
        )
        slots = _get_available_slots(next_monday)
        self.assertEqual(len(slots), 2)  # 09:00 and 09:30
