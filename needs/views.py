from django.shortcuts import HttpResponse
from django.core.management import call_command
from .models import NeedType, Lead
from covid.renderer import renderView

def index(request):
    needs = NeedType.objects.all()
    return renderView(request,'needs.html',{"needs":needs})

def needs(request,need=None):
    try:
        needobj = NeedType.objects.get(id=need)
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

def callCommand(request,argv):
    commands = {"sync_sheets":"python manage.py syncgsheets"}
    try:
        output = "The result is: "
        output += call_command(commands[argv])
        return HttpResponse(" ".join(i for i in output))
    except Exception as e:
        print(e)
        return HttpResponse("There is not such command")
