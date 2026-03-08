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


class Project(models.Model):
    SERVICE_CHOICES = [
        ('aerial', 'Aerial Photography'),
        ('survey', 'Drone Survey'),
        ('inspection', 'Inspection'),
        ('mapping', 'Mapping'),
        ('construction', 'Construction Tracking'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    client_name = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, blank=True)
    main_image = models.ImageField(upload_to='projects/')
    completion_date = models.DateField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.title} - Image {self.id}"
