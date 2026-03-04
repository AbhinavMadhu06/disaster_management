import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
django.setup()

from django.test import RequestFactory
from myapp.views import public_chatbot_response

factory = RequestFactory()
body = json.dumps({
    "message": "Hello",
    "lid": 1, 
    "latitude": "0", "longitude": "0", "weather": None
})

request = factory.post('/myapp/public_chatbot_response/', content_type='application/json', data=body)
response = public_chatbot_response(request)
print("Status:", response.status_code)
print("Content:", response.content)
