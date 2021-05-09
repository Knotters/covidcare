from django.shortcuts import render, HttpResponse
from . import env

def renderData(request,view,data={}):
    data['appname'] = env.PUBNAME
    return render(request,view,data)

def index(request):
    return renderData(request,'index.html')