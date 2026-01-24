from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

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

            inquiry.save()  # Now save with the IP
            # Send Email Notification
            send_mail(
                subject=f"New Drone Lead: {inquiry.name}",
                message=f"You have a new inquiry from {inquiry.name} ({inquiry.email}):\nIP: {inquiry.ip_address}\n\n{inquiry.message}",
                from_email=settings.EMAIL_HOST_USER,
                # Where you want to get the alert
                recipient_list=['ajsawyer94@gmail.com'],
            )
            return redirect('main:home')  # Redirect after success
    else:
        form = ContactForm()

    return render(request, 'main/home.html', {'form': form})
