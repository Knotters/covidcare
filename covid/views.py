from django.shortcuts import render, HttpResponse, redirect
from django.middleware import csrf
from . import env
import requests
from django.contrib.sessions.models import Session


def renderData(request, view, data={}):
    data['appname'] = env.PUBNAME
    return render(request, view, data)


def index(request):
    return renderData(request, 'index.html')


def checkSession():
    session = Session.objects.all()


def doc(f):
    def wrap(request, *args, **kwargs):
        if 'userid' not in request.session.keys():
            sessionID = requests.post(f'{env.SUPERDOMAIN}/auth/getuser').json()
            print(str(sessionID))
            if sessionID:
                session = Session.objects.get(session_key=sessionID).using('super')
                user = session.session_data.get_decoded()
                print(user)
            return f(request, *args, **kwargs)

    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap

@doc
def private(request):
    print(request.user)
    return HttpResponse("private")
    # if request.session.has_keys('username'):
    # return redirect('http://127.0.0.1:8000/subdomain/authcheck/?next=http://127.0.0.1:5000/private')


