from django.shortcuts import redirect
from .env import SUPERDOMAIN
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,Http404,HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth import login, authenticate,logout

def superlogin(f):
    def wrap(request, *args, **kwargs):
        try:
            sessionID = request.COOKIES['sessionid']
            if sessionID:
                if request.session.has_key('user'):
                    print("yes")
                    return f(request, *args, **kwargs)
                else:
                    session = Session.objects.filter(session_key=str(sessionID)).using('super')
                    print(session)
                    for s in session:
                        decoded = s.get_decoded()
                        print(decoded)
                        user = User.objects.filter(id=decoded["_auth_user_id"]).using('super')
                        print("this",user)
                        request.session['user'] = str(user[0])
                        request.session['name'] = str(user[0].first_name) + str(user[0].last_name)
                        break
                    return f(request, *args, **kwargs)
            else:
                return redirect(f'{SUPERDOMAIN}/accounts/login/?next={request.build_absolute_uri()}')
        except:
            return redirect(f'{SUPERDOMAIN}/accounts/login/?next={request.build_absolute_uri()}')
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap
