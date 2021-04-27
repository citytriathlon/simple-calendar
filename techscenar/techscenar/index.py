from django.http import HttpResponse
from django.shortcuts import render
from . import ics_read

def mainpage(request):
    context = ics_read.get_next_item()
    return render(request, 'index.html', {'data': context})