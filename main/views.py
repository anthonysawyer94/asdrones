from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import ContactForm

# Create your views here.


def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # You can access data here: name = form.cleaned_data['name']
            # Create the object but don't save to DB yet
            inquiry = form.save(commit=False)

            # Get the IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                inquiry.ip_address = x_forwarded_for.split(',')[0]
            else:
                inquiry.ip_address = request.META.get('REMOTE_ADDR')

            inquiry.save()
            try:
                send_mail(
                    subject=f"New Drone Lead: {inquiry.name}",
                    message=f"You have a new inquiry from {inquiry.name} ({inquiry.email}):\nIP: {inquiry.ip_address}\n\n{inquiry.message}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
                )
            except Exception:
                messages.error(request, "Your inquiry was saved but email notification failed. We'll still get back to you.")
            return redirect('main:home')
    else:
        form = ContactForm()

    return render(request, 'main/home.html', {'form': form})

# Error Handlers


def custom_404(request, exception):
    return render(request, 'main/404.html', status=404)


def custom_403(request, exception):
    return render(request, 'main/403.html', status=403)


def custom_500(request):
    return render(request, 'main/500.html', status=500)


def csrf_failure(request, reason=""):
    return render(request, 'main/403.html', status=403)
