from .env import PUBNAME, SITE, SUPERDOMAIN, MAILUSER
from django.shortcuts import render

def renderView(request, view, data={}):
    data['appname'] = PUBNAME
    data['description'] = "Covid pandemic related help resouces for people in need."
    data['site'] = SITE
    data['superdom'] = SUPERDOMAIN
    data['contactmail'] = MAILUSER
    return render(request, view, data)
