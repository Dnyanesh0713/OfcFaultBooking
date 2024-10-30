# middleware/auto_logout.py
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
import datetime


class AutoLogout(MiddlewareMixin):
    def process_request(self, request):
        # Time in seconds for auto-logout
        timeout = getattr(settings, 'SESSION_COOKIE_AGE', 300)

        # If user is authenticated
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            now = datetime.datetime.now().timestamp()

            if last_activity and (now - last_activity > timeout):
                # Logout the user due to inactivity
                logout(request)
                del request.session['last_activity']
                return redirect('/login/?timeout=1')  # Redirect to login with timeout notice

            # Update the last activity timestamp
            request.session['last_activity'] = now
