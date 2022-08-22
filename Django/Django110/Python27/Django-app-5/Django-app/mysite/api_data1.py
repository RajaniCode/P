# Django-app-2
# Playing with the API and sqlite # Without python manage.py runserver # Python shell
# Bypassing manage.py
# Run python from the same directory manage.py

import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

from polls.models import Question, Choice   # Import the model classes we just wrote.

# No questions are in the system yet.
print(Question.objects.all())
# <QuerySet []>

# Create a new Question.
# Support for time zones is enabled in the default settings file, so
# Django expects a datetime with tzinfo for pub_date. Use timezone.now()
# instead of datetime.datetime.now() and it will do the right thing.
from django.utils import timezone
q = Question(question_text="What's new?", pub_date=timezone.now())

# Save the object into the database. You have to call save() explicitly.
q.save()

# Now it has an ID. Note that this might say "1L" instead of "1", depending
# on which database you're using. That's no biggie; it just means your
# database backend prefers to return integers as Python long integer
# objects.
print(q.id)
# 1

# Access model field values via Python attributes.
print(q.question_text)
# "What's new?"
print(q.pub_date)
# datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)

# Change values by changing the attributes, then calling save().
q.question_text = "What's up?"
q.save()

# objects.all() displays all the questions in the database.
print(Question.objects.all())
# <QuerySet [<Question: Question object>]>
