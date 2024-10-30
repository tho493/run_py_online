from django.shortcuts import render
from django.http import HttpResponse


def index(request):
   return render(request, 'index.html')

def add_test_part(request):
   return render(request, 'add_test_part.html')