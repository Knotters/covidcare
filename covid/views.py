from covid.decorators import superlogin
from django.shortcuts import HttpResponse, redirect
from .renderer import renderView
from .env import SUPERDOMAIN
from django.contrib.auth.models import User
from needs.models import NeedType, Lead, Alert, Latest, Video, FAQ


def index(request):
    alerts = Alert.objects.all()
    needs = NeedType.objects.all()
    latests = Latest.objects.all()
    videos = Video.objects.all()
    faqs = FAQ.objects.all()
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
        "faqs":faqs
    })

# @superlogin
def volunteer(request):
    return renderView(request, 'volunteer.html')
