from django.shortcuts import HttpResponse
from .renderer import renderView
from .decorators import require_superlogin
from django.contrib.sessions.models import Session


def index(request):
    return renderView(request, 'index.html')

@require_superlogin
def private(request):    
    return HttpResponse("private")
