import requests
from django.http import HttpResponse

class InternetConnectivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check internet connectivity
        try:
            # Perform a simple GET request to a reliable site like Google
            requests.get("https://www.google.com", timeout=4)
        except (requests.ConnectionError, requests.Timeout):
            # Return a custom response if there's no internet
            return HttpResponse(
                "<h1>Internet Connection Required, Please Activate proxy using address http://10.64.4.12 and port 8080 in your proxy setting...</h1><p>Please connect to the internet to access this application.</p>",
                content_type="text/html",
                status=503
            )
        # Proceed with the request if there's internet
        response = self.get_response(request)
        return response
