from django.shortcuts import render
from django.http import HttpResponse
# Create your view here.

def home(request):
    return HttpResponse("Hello World1")