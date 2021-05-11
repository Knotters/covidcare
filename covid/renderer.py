from .env import PUBNAME, SUPERDOMAIN, MAILUSER
from django.shortcuts import render

def renderView(request, view, data={}):
    data['appname'] = PUBNAME
    data['superdom'] = SUPERDOMAIN
    data['contactmail'] = MAILUSER
    return render(request, view, data)
