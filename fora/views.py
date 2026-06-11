import datetime
from datetime import date, time, timedelta

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BookingForm
from .models import Availability, Consultation


def _to_time(value):
    """Convert a TimeField value (time or str) to a datetime.time object."""
    if isinstance(value, str):
        parts = value.split(":")
        return time(int(parts[0]), int(parts[1]))
    return value


def _get_available_slots(target_date):
    """Return list of available 30-min time slots for a given date."""
    weekday = target_date.weekday()
    avail_blocks = Availability.objects.filter(day_of_week=weekday, is_active=True)

    if not avail_blocks:
        return []

    booked = Consultation.objects.filter(
        date=target_date, status__in=["pending", "approved"]
    ).values_list("time", flat=True)
    booked_times = {_to_time(t) for t in booked}

    slots = []
    for block in avail_blocks:
        current = datetime.datetime.combine(target_date, _to_time(block.start_time))
        end = datetime.datetime.combine(target_date, _to_time(block.end_time))
        while current + timedelta(minutes=30) <= end:
            slot_time = current.time()
            if slot_time not in booked_times:
                slots.append(slot_time)
            current += timedelta(minutes=30)
    return slots


def book_view(request):
    min_date = timezone.localdate() + timedelta(days=1)
    available_dates = []
    for i in range(60):
        d = min_date + timedelta(days=i)
        if Availability.objects.filter(
            day_of_week=d.weekday(), is_active=True
        ).exists():
            available_dates.append(d)

    selected_date = None
    available_slots = []

    if request.method == "POST":
        form = BookingForm(request.POST)
        date_str = request.POST.get("date", "")
        time_str = request.POST.get("time", "")

        try:
            selected_date = date.fromisoformat(date_str)
        except (ValueError, TypeError):
            selected_date = None

        if selected_date and selected_date < min_date:
            messages.error(
                request, "Bookings must be made at least one day in advance."
            )
            return render(
                request,
                "fora/book.html",
                {
                    "form": form,
                    "available_dates": available_dates,
                    "selected_date": selected_date,
                    "available_slots": _get_available_slots(selected_date)
                    if selected_date
                    else [],
                },
            )

        if form.is_valid() and selected_date and time_str:
            try:
                slot_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            except (ValueError, TypeError):
                messages.error(request, "Invalid time selected.")
                return render(
                    request,
                    "fora/book.html",
                    {
                        "form": form,
                        "available_dates": available_dates,
                        "selected_date": selected_date,
                        "available_slots": _get_available_slots(selected_date)
                        if selected_date
                        else [],
                    },
                )

            if slot_time not in _get_available_slots(selected_date):
                messages.error(
                    request,
                    "That time slot is no longer available. Please choose another.",
                )
                return render(
                    request,
                    "fora/book.html",
                    {
                        "form": form,
                        "available_dates": available_dates,
                        "selected_date": selected_date,
                        "available_slots": _get_available_slots(selected_date)
                        if selected_date
                        else [],
                    },
                )

            consultation = form.save(commit=False)
            consultation.date = selected_date
            consultation.time = slot_time
            consultation.save()

            messages.success(
                request,
                "Your consultation has been requested! You'll receive a confirmation email once approved.",
            )
            return redirect("fora:confirmation", pk=consultation.pk)

    else:
        form = BookingForm()
        date_str = request.GET.get("date", "")
        if date_str:
            try:
                selected_date = date.fromisoformat(date_str)
                if selected_date >= min_date:
                    available_slots = _get_available_slots(selected_date)
            except (ValueError, TypeError):
                pass

    return render(
        request,
        "fora/book.html",
        {
            "form": form,
            "available_dates": available_dates,
            "selected_date": selected_date,
            "available_slots": available_slots,
        },
    )


def confirmation_view(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    return render(request, "fora/confirmation.html", {"consultation": consultation})
