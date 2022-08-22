# from django.shortcuts import render
# Django-app-1
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
