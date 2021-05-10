from django.shortcuts import redirect
from .env import SUPERDOMAIN

def require_superlogin(f):
    def wrap(request, *args, **kwargs):
        try:
            sessionID = request.COOKIES['sessionid']
            if sessionID:
                # session = Session.objects.get(session_key=sessionID).using('super')
                # user = session.session_data.get_decoded()
                # print(user)
                return f(request, *args, **kwargs)
        except:
            return redirect(f'{SUPERDOMAIN}/accounts/login/?next={request.build_absolute_uri()}')
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap