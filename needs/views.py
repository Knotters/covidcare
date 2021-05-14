from django.http.response import Http404
from django.shortcuts import HttpResponse
from django.core.management import call_command
from .models import NeedType, Lead, State, District
from covid.renderer import renderView


def index(request):
    needs = NeedType.objects.all()
    return renderView(request, 'needs.html', {"needs": needs})


def needs(request, need=None):
    try:
        needobj = NeedType.objects.get(id=need)
        states = State.objects.all()
        districts = []
        try:
            resources = Lead.objects.filter(needtype=needobj)
        except:
            resources = []
        try:
            statename = str(request.GET['state'])
            state = State.objects.get(name=statename)
            districts = District.objects.filter(state=state)
            resources = resources.filter(state=state)
        except:
            state = None
        try:
            distname = str(request.GET['district'])
            if state:
                district = District.objects.get(name=distname,state=state)
            else:
                district = District.objects.get(name=distname)
            if district:
                resources = resources.filter(district=district)
        except:
            district = None

        return renderView(request, 'leads.html', {
            'leads': resources,
            'need': needobj,
            "states":states,
            "districts":districts,
            "state": state,
            "district": district
        })
    except:
        raise Http404()


def callCommand(request, argv):
    commands = {"sync_sheets": "python manage.py syncgsheets"}
    try:
        output = "The result is: "
        output += call_command(commands[argv])
        return HttpResponse(" ".join(i for i in output))
    except Exception as e:
        print(e)
        return HttpResponse("There is not such command")
