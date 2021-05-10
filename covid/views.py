from django.shortcuts import HttpResponse
from .renderer import renderView
from .decorators import require_superlogin
from django.contrib.sessions.models import Session

from needs.models import NeedType, Lead

def index(request):
    needs = NeedType.objects.all()
    newneeds = []
    i = 1
    for need in needs:
        if i < 8:
            newneeds.append(need)
        i+=1
    totalproviders = Lead.objects.all().count()
    return renderView(request, 'index.html', { "needs": newneeds, "totalproviders":totalproviders })

@require_superlogin
def private(request):    
    return HttpResponse("private")
