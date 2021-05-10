from django.shortcuts import HttpResponse
from .renderer import renderView
from .decorators import require_superlogin
from django.contrib.sessions.models import Session

from needs.models import NeedType

def index(request):
    needs = NeedType.objects.all()
    return renderView(request, 'index.html', { "needs": needs })

@require_superlogin
def private(request):    
    return HttpResponse("private")
