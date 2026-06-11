from django.contrib import admin, messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Availability, Consultation


@admin.action(description="Approve selected consultations")
def approve_consultations(modeladmin, request, queryset):
    for consultation in queryset.filter(status="pending"):
        consultation.status = "approved"
        consultation.save()

        subject = "Your Consultation with Fora Travel Advisor Has Been Confirmed!"
        html_message = render_to_string(
            "fora/email_approved.html", {"consultation": consultation}
        )
        plain_message = (
            f"Hi {consultation.name},\n\n"
            f"Your 30-minute consultation has been confirmed for "
            f"{consultation.date.strftime('%A, %B %d, %Y')} at "
            f"{consultation.time.strftime('%I:%M %p')}.\n\n"
            f"I look forward to speaking with you!\n\n"
            f"Best,\nAnthony Sawyer\nFora Travel Advisor"
        )

        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=None,
                recipient_list=[consultation.email],
                html_message=html_message,
                fail_silently=False,
            )
            modeladmin.message_user(
                request, f"Approved and emailed {consultation.name}.", messages.SUCCESS
            )
        except Exception as e:
            modeladmin.message_user(
                request,
                f"Approved {consultation.name} but email failed: {e}",
                messages.WARNING,
            )


@admin.action(description="Decline selected consultations")
def decline_consultations(modeladmin, request, queryset):
    for consultation in queryset.filter(status="pending"):
        consultation.status = "declined"
        consultation.save()

        subject = "Your Consultation Request Update"
        plain_message = (
            f"Hi {consultation.name},\n\n"
            f"Unfortunately, your consultation request for "
            f"{consultation.date.strftime('%A, %B %d, %Y')} at "
            f"{consultation.time.strftime('%I:%M %p')} could not be accommodated.\n\n"
            f"Please feel free to book another time slot.\n\n"
            f"Best,\nAnthony Sawyer\nFora Travel Advisor"
        )

        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=None,
                recipient_list=[consultation.email],
                fail_silently=False,
            )
            modeladmin.message_user(
                request, f"Declined and notified {consultation.name}.", messages.SUCCESS
            )
        except Exception as e:
            modeladmin.message_user(
                request,
                f"Declined {consultation.name} but email failed: {e}",
                messages.WARNING,
            )


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ["day_of_week", "start_time", "end_time", "is_active"]
    list_editable = ["is_active"]
    list_filter = ["day_of_week", "is_active"]
    ordering = ["day_of_week", "start_time"]


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "date", "time", "status", "created_at"]
    list_filter = ["status", "date"]
    search_fields = ["name", "email"]
    date_hierarchy = "date"
    actions = [approve_consultations, decline_consultations]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        ("Client Info", {"fields": ["name", "email", "phone", "notes"]}),
        ("Appointment", {"fields": ["date", "time", "status"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"]}),
    ]
