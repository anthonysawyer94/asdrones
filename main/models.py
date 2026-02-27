from django.db import models


class ProjectInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Review(models.Model):
    SERVICE_CHOICES = [
        ('aerial', 'Aerial Photography'),
        ('survey', 'Drone Survey'),
        ('inspection', 'Inspection'),
        ('mapping', 'Mapping'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating} stars ({self.get_service_type_display()})"
