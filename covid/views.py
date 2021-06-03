from .renderer import renderView
from django.http.response import Http404
from needs.models import *


def index(request):
    alerts = Alert.objects.all()
    needs = NeedType.objects.all()
    latests = Latest.objects.all()
    videos = Video.objects.all()
    newvideos = []
    i = 1
    for video in videos:
        if i < 4:
            newvideos.append(video)
        i += 1
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
        "videos": newvideos,
        "faqs": faqs,
        "phones": phones
    })


def mediaclips(request):
    videos = Video.objects.all()
    return renderView(request, 'media.html', {
        "videos": videos,
    })


def volunteer(request):
    raise Http404()
