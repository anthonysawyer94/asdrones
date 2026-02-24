# AGENTS.md - Developer Guide for AS Drones

This file provides guidelines and instructions for agentic coding agents working on this codebase.

## Project Overview

This is a Django 6.0.1 project for a drone services website. It uses SQLite for development and supports dev, stage, and prod environments.

## Technology Stack

- **Python**: 3.11+
- **Django**: 6.0.1
- **Database**: SQLite (dev), PostgreSQL (prod/stage)
- **Virtual Environment**: `venv`

---

## Build, Lint, and Test Commands

### Virtual Environment Setup

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements/dev.txt
```

### Running the Development Server

```bash
# Standard development
python manage.py runserver

# With specific port
python manage.py runserver 8080
```

### Database Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations (use appropriate manage script)
python manage.py migrate          # Dev
python manage.stage.py migrate    # Stage
python manage.prod.py migrate     # Prod
```

### Collecting Static Files

```bash
python manage.prod.py collectstatic
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test main

# Run a specific test class
python manage.py test main.tests.MyTestClass

# Run a specific test method
python manage.py test main.tests.MyTestClass.test_my_method

# Run with verbosity
python manage.py test -v 2
```

### Running Django Management Commands

```bash
# Create superuser
python manage.py createsuperuser

# Check for issues
python manage.py check

# Show URLs
python manage.py show_urls
```

---

## Code Style Guidelines

### General Conventions

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters (soft limit)
- Use meaningful, descriptive names for variables and functions
- Add docstrings to all public functions and classes

### Import Organization

Order imports as follows (with a blank line between groups):

1. Standard library imports
2. Third-party imports
3. Django imports
4. Local application imports

Example:
```python
import os
import sys

from django.db import models
from django.conf import settings

from .models import MyModel
from .forms import MyForm
```

### Django-Specific Guidelines

#### Models (`models.py`)

- Use `models.Model` as base class
- Define `__str__` method for all models
- Use appropriate field types (`CharField`, `TextField`, `EmailField`, `GenericIPAddressField`, etc.)
- Add `null=True` only when necessary (use empty strings for text fields)
- Use `auto_now_add` for creation timestamps, `auto_now` for modification timestamps

Example:
```python
class ProjectInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
```

#### Views (`views.py`)

- Use function-based views or class-based views consistently
- Always handle both GET and POST methods in forms
- Use `redirect` after successful form submissions
- Use `form.is_valid()` before accessing `cleaned_data`
- Return appropriate HTTP status codes (200, 404, 403, 500)

#### Forms (`forms.py`)

- Use `forms.ModelForm` for model-backed forms
- Define `Meta` class with `model` and `fields`
- Add custom validation in `clean()` method if needed

#### URLs (`urls.py`)

- Use named URL patterns: `name='app:view_name'`
- Use `app_name` namespace for each app

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Variables | snake_case | `my_variable` |
| Functions | snake_case | `get_user_data` |
| Classes | PascalCase | `ProjectInquiry` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Django apps | lowercase | `main` |
| Models | PascalCase | `ProjectInquiry` |
| Database fields | snake_case | `ip_address` |

### Error Handling

- Use try/except blocks for operations that may fail
- Catch specific exceptions rather than using bare `except`
- Log errors appropriately using Django's logging
- Return user-friendly error messages in views
- Create custom error templates (404.html, 403.html, 500.html)

Example:
```python
try:
    inquiry.save()
except IntegrityError:
    # Handle duplicate entry
    pass
```

### Testing

- Use Django's built-in `django.test.TestCase`
- Name test methods with `test_` prefix
- Use `self.assertEqual`, `self.assertTrue`, etc.
- Test both success and failure cases
- Include docstrings for test classes and complex test methods

Example:
```python
from django.test import TestCase
from django.urls import reverse


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
```

### Settings Configuration

- Development settings: `asdrones/conf/dev.py`
- Stage settings: `asdrones/conf/stage.py`
- Production settings: `asdrones/conf/prod.py`
- Never commit secrets to version control
- Use environment variables for sensitive data (see `.env.dev`, `.env.prod`)

### File Organization

```
asdrones/
├── asdrones/              # Project configuration
│   ├── conf/              # Settings (dev, stage, prod)
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI config
├── main/                  # Main Django app
│   ├── migrations/        # Database migrations
│   ├── models.py          # Database models
│   ├── views.py           # Views
│   ├── forms.py           # Forms
│   ├── urls.py            # App URLs
│   ├── admin.py           # Admin configuration
│   └── tests.py           # Tests
├── manage.py              # Dev management script
├── manage.prod.py         # Prod management script
├── manage.stage.py        # Stage management script
└── requirements/          # Dependency files
```

---

## Additional Notes

- This project uses `django-debug-toolbar` in development
- Static files are served via `whitenoise` in production
- Email is configured via Django's email settings
- IP addresses are captured for inquiry tracking
