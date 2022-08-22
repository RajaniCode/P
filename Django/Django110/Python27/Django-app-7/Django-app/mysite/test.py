# Playing with the API and sqlite # Without python manage.py runserver # Python shell
# Bypassing manage.py
# Run python from the same directory manage.py

import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

# Django-app-5
import datetime
from django.utils import timezone
from polls.models import Question

# create a Question instance with pub_date 30 days in the future
future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
print(future_question.was_published_recently())
