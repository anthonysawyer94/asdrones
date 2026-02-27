import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django_ratelimit import UNSAFE

from .forms import ContactForm, ReviewForm
from .models import Review

logger = logging.getLogger(__name__)


@ratelimit(key='ip', rate='3/h', method='POST', block=True)
def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        honeypot = request.POST.get('website', '')
        if honeypot:
            logger.info(f"Honeypot triggered - potential bot from {request.META.get('REMOTE_ADDR')}")
            return redirect('main:home')
        
        if form.is_valid():
            inquiry = form.save(commit=False)

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                inquiry.ip_address = x_forwarded_for.split(',')[0]
            else:
                inquiry.ip_address = request.META.get('REMOTE_ADDR')

            inquiry.save()

            try:
                send_mail(
                    subject=f"New Drone Lead: {inquiry.name}",
                    message=f"You have a new inquiry from {inquiry.name} ({inquiry.email}):\nIP: {inquiry.ip_address}\nPhone: {inquiry.phone}\n\n{inquiry.message}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
                )
            except Exception as e:
                logger.error(f"Failed to send email for inquiry {inquiry.id}: {e}")

            messages.success(request, "Thank you! We'll be in touch soon.")
            return redirect('main:home')
    else:
        form = ContactForm()

    return render(request, 'main/home.html', {'form': form})


def reviews(request):
    approved_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'main/reviews.html', {'reviews': approved_reviews})


def leave_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your review! It will be posted after approval.")
            return redirect('main:reviews')
    else:
        form = ReviewForm()

    return render(request, 'main/leave_review.html', {'form': form})


def custom_404(request, exception):
    return render(request, 'main/404.html', status=404)


def custom_403(request, exception):
    return render(request, 'main/403.html', status=403)


def custom_500(request):
    return render(request, 'main/500.html', status=500)


def csrf_failure(request, reason=""):
    return render(request, 'main/403.html', status=403)
