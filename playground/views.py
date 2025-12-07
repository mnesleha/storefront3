from django.core.cache import cache
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
import os
import requests
import logging

logger = logging.getLogger(__name__)


class HelloView(APIView):
    def send_simple_message(self, request):
        response = requests.post(
            "https://api.mailgun.net/v3/sandbox36f38199cfaf4f75b345859e5239f699.mailgun.org/messages",
            auth=("api", os.getenv('API_KEY', 'API_KEY')),
            data={"from": "Mailgun Sandbox <postmaster@sandbox36f38199cfaf4f75b345859e5239f699.mailgun.org>",
                  "to": "Heroku <812cd309-fa07-474d-8481-cd8523341f6a@heroku.com>",
                  "subject": "Hello Heroku",
                  "text": "Congratulations Heroku, you just sent an email with Mailgun! You are truly awesome!"})

    def get(self, request):
        return render(request, 'hello.html', {'name': self.send_simple_message(request)})

    # cache na class based view, logging
    # @method_decorator(cache_page(5 * 60))
    # def get(self, request):
    #     try:
    #         logger.debug("Fetching data from https://httpbin.org/delay/2")
    #         response = requests.get('https://httpbin.org/delay/2')
    #         logger.debug("Data fetched successfully")
    #         data = response.json()
    #     except requests.ConnectionError:
    #         logger.critical("Failed to connect to external service")
    #     return render(request, 'hello.html', {'name': data})


# cache na API view
# @cache_page(5 * 60)
# def say_hello(request):
#     response = requests.get('https://httpbin.org/delay/2')
#     data = response.json()
#     return render(request, 'hello.html', {'name': data})


# použítí fake smtp serveru na lokálním počítači pro testování emailů
    # try:
    #     # Render the template manually
    #     html_content = render_to_string('emails/hello.html', {'name': 'Mosh'})

    #     message = EmailMessage(
    #         subject='Hello from Django',
    #         body=html_content,
    #         to=['john@example.com']
    #     )
    #     message.content_subtype = 'html'  # Set content type to HTML

    #     # Use absolute path
    #     file_path = os.path.join(
    #         settings.BASE_DIR, 'playground', 'static', 'images', 'logo.png')
    #     message.attach_file(file_path)
    #     message.send()
    # except ValueError:
    #     pass
    # return render(request, 'hello.html', {'name': 'Mosh'})
