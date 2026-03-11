import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
django.setup()

from django.db import connection
from myapp.models import Chatbot, DonateGoods, News_reporter, Public

with connection.schema_editor() as schema_editor:
    models_to_create = [Chatbot, DonateGoods, News_reporter, Public]
    for model in models_to_create:
        try:
            schema_editor.create_model(model)
            print(f"Created table for {model.__name__}")
        except Exception as e:
            print(f"Failed to create table for {model.__name__}: {e}")
