from .env import PUBNAME, SUPERDOMAIN
from django.shortcuts import render

def renderView(request, view, data={}):
    data['appname'] = PUBNAME
    data['superdom'] = SUPERDOMAIN
    return render(request, view, data)
