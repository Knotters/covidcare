from django.shortcuts import HttpResponse
from .models import NeedType, Lead
from covid.renderer import renderView

def index(request):
    needs = NeedType.objects.all()
    return renderView(request,'needs.html',{"needs":needs})

def needs(request,need=None):
    try:
        needobj = NeedType.objects.get(type=need)
        try:
            resources = Lead.objects.filter(needtype=needobj)
        except:
            resources = []
        try:
            request.GET['verified']
            verified = True
            resources = resources.filter(verified=True)
        except:
            verified = False
        return renderView(request, 'leads.html', { 'leads': resources, 'need': needobj, 'verified':verified }) 
    except:
        return HttpResponse("No such need")

