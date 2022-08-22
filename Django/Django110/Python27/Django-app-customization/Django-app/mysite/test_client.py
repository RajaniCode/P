# Playing with the API and sqlite # Without python manage.py runserver # Python shell
# Bypassing manage.py
# Run python from the same directory manage.py

import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

from django.test.utils import setup_test_environment
setup_test_environment()

from django.test import Client
# create an instance of the client for our use
client = Client()

# get a response from '/'
response = client.get('/')
# we should expect a 404 from that address
print(response.status_code)

# on the other hand we should expect to find something at '/polls/'
# we'll use 'reverse()' rather than a hardcoded URL
from django.urls import reverse
response = client.get(reverse('polls:index'))
print(response.status_code)
print(response.content)

# note - you might get unexpected results if your ``TIME_ZONE``
# in ``settings.py`` is not correct. If you need to change it,
# you will also need to restart your shell session
from polls.models import Question
from django.utils import timezone
# create a Question and save it
q = Question(question_text="Who is your favorite Beatle?", pub_date=timezone.now())
q.save()
# check the response once again
response = client.get('/polls/')
print(response.content)

# If the following doesn't work, you probably omitted the call to
# setup_test_environment() described above
print(response.context['latest_question_list'])


# http://127.0.0.1:8000/admin/polls/question/
# Home > Polls > Questions > Delete multiple objects
# Action: Delete selected questions
# Go
# QUESTION
# Who is your favorite Beatle?
