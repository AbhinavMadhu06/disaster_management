import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
django.setup()

from django.test import RequestFactory
from myapp.views import public_chatbot_response

factory = RequestFactory()

# Simulating the exact payload from Flutter's publicChatScreen.dart
body = json.dumps({
    'message': 'Hello from Flutter',
    'lid': '',
    'latitude': '10.0',
    'longitude': '20.0',
    'weather': None
})

request = factory.post('/myapp/public_chatbot_response/', content_type='application/json', data=body)
response = public_chatbot_response(request)

print(f"Status Code: {response.status_code}")
if response.status_code != 200:
    print(f"Error Response: {response.content}")
else:
    print(f"Success Response: {response.content}")
