from covid.decorators import superlogin
from .renderer import renderView
from django.contrib.auth.models import User
from needs.models import *


def index(request):
    alerts = Alert.objects.all()
    needs = NeedType.objects.all()
    latests = Latest.objects.all()
    videos = Video.objects.all()
    faqs = FAQ.objects.all()
    phones = Phoneline.objects.all()
    newneeds = []
    i = 1
    for need in needs:
        if i < 8:
            newneeds.append(need)
        i += 1
    totalproviders = Lead.objects.all().count()
    return renderView(request, 'index.html', {
        "needs": newneeds,
        "totalproviders": totalproviders,
        "alerts": alerts,
        "latests": latests, 
        "videos":videos,
        "faqs":faqs, 
        "phones":phones
    })

@superlogin
def volunteer(request):
    return renderView(request, 'volunteer.html')
