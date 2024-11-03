from django.utils import timezone
from django.conf import settings

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timezone.activate(settings.TIME_ZONE)  # Set timezone to 'Asia/Kolkata'
        response = self.get_response(request)
        timezone.deactivate()  # Deactivate after response
        return response
