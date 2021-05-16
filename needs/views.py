from django.http.response import Http404
from django.shortcuts import HttpResponse
from django.core.management import call_command
from .models import NeedType, Lead, State, District
from covid.renderer import renderView
from django.contrib.auth.decorators import user_passes_test
import gspread
from gspread.models import Worksheet
from covid import env
from fuzzywuzzy import process

# def getState(state):
#     state_list = State.objects.values_list("name")
#     state_list = [i[0] for i in state_list]
#     Ratios = process.extract(state,state_list)
#     finalvalue = max(Ratios,key=lambda x:x[1])
#     print(finalvalue)


def getDistrict(district):
    district_list = District.objects.values_list("name")
    district_list = [i[0] for i in district_list]
    Ratios = process.extract(district,district_list)
    finalvalue = max(Ratios,key=lambda x:x[1])
    districtobj = District.objects.get(name=finalvalue[0])
    print(districtobj.name,districtobj.state)
    return districtobj

getDistrict("Papumpare")
gc = gspread.service_account(filename=env.GOOGLE_CRED)
sh = gc.open_by_key(env.SPREADSHEETID)

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

@user_passes_test(lambda u: u.is_superuser)
def addOxygens(request):
    Worksheet = sh.worksheet("Oxygen")
    res = Worksheet.get_all_records()
    print(res[0])
    oxy = NeedType.objects.get(type="Oxygen")
    newlyaded = 0
    updated = 0
    count = 0
    for i in res:
        if(count==1):
            break
        sr_no = str(i["Sr. No."])
        try:
            obj = getDistrict(i["District"])
            district,state = obj,obj.state
        except:
            district,state = None,None
        if(sr_no.strip()!=""):
            uuid = i["UUID"]
            if(uuid.strip()==""):
                oxygenobj = Lead.objects.create(needtype=oxy,provider=i["Provider"],contact=i["Contact"],state=state,district=district,address=i["Address"],name=i["Name"])
                oxygenobj.save()
                newlyaded+=1
            else:
                try:
                    oxygenobj = Lead.objects.get(id=uuid)
                    oxygenobj.needtype=oxy
                    oxygenobj.provider=i["Provider"]
                    oxygenobj.contact=i["Contact"]
                    oxygenobj.state=state
                    oxygenobj.district=district
                    oxygenobj.address=i["Address"]
                    oxygenobj.save()
                    updated+=1
                except:
                    pass
            count+=1

    return HttpResponse({"Added":newlyaded,"Updated":updated})