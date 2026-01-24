from django.conf import settings


def project_context(request):
    context = {
        'my_email': 'ajsawyer94@gmail.com',
        'PRODUCTION': getattr(settings, 'PRODUCTION', False),
    }
    return context
