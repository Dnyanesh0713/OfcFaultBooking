from django.db import models
from django.utils import timezone


class FormattedDateTimeField(models.DateTimeField):
    def to_python(self, value):
        # Converts the datetime to local timezone when retrieved
        value = super().to_python(value)
        if isinstance(value, timezone.datetime):
            return timezone.localtime(value)
        return value

    def value_to_string(self, obj):
        # Formats the datetime without seconds and timezone
        value = self.value_from_object(obj)
        if value:
            value = timezone.localtime(value)  # Ensure it’s in local timezone
            return value.strftime("%d-%m-%Y :: %I:%M %p")
        return ''
