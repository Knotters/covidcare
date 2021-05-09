from django.shortcuts import render, HttpResponse
from .models import NeedType, Lead

def renderData(request,view,data={}):
    # data['appname'] = env.PUBNAME
    return render(request,view,data)

def index(request):
    needs = NeedType.objects.all()
    return renderData(request,'needs.html',{"needs":needs})

def needs(request,need=None):
    try:
        needobj = NeedType.objects.get(type=need)
        try:
            resources = Lead.objects.filter(needtype=needobj)
        except:
            resources = []
        return renderData(request, 'leads.html', { 'leads': resources, 'need': needobj })
    except:
        return HttpResponse("No such need")


