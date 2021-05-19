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


def getState(state):
    state_list = State.objects.values_list("name")
    state_list = [i[0] for i in state_list]
    Ratios = process.extract(state, state_list)
    finalvalue = max(Ratios, key=lambda x: x[1])
    stateobj = State.objects.get(name=finalvalue[0])
    return stateobj


def getDistrict(district):
    district_list = District.objects.values_list("name")
    district_list = [i[0] for i in district_list]
    Ratios = process.extract(district, district_list)
    finalvalue = max(Ratios, key=lambda x: x[1])
    if(finalvalue[1] < 80):
        return False
    districtobj = District.objects.get(name=finalvalue[0])
    return districtobj


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
                district = District.objects.get(name=distname, state=state)
            else:
                district = District.objects.get(name=distname)
            if district:
                resources = resources.filter(district=district)
        except:
            district = None

        return renderView(request, 'leads.html', {
            'leads': resources,
            'need': needobj,
            "states": states,
            "districts": districts,
            "state": state,
            "district": district
        })
    except:
        raise Http404()


def addLeads(request):
    output_list = []
    try:
        key = request.GET["key"]
        if(str(key) != str(env.PROJECTKEY)):
            return Http404()
    except:
        return Http404()
    newlyadded = 0
    updated = 0
    try:
        gc = gspread.service_account(filename=env.GOOGLE_CRED)
        sh = gc.open_by_key(env.SPREADSHEETID)
        need_types = NeedType.objects.all()
        for need in need_types:
            try:
                Worksheet = sh.worksheet(need.type.capitalize())
                print(f"Worksheet found: {need.type}")
            except:
                output_list.append(f"Worksheet not found: {need.type}")
                continue
            res = Worksheet.get_all_records()
            for i in res:
                sr_no = str(i["Sr. No."])
                try:
                    districts = str(i["District"]).split(",")
                    for dis in districts:
                        obj = getDistrict(dis)
                        if(obj == False):
                            continue
                        district, state = obj, obj.state
                        if(sr_no.strip() != ""):
                            uuid = i["UUID"]
                            if(uuid.strip() == ""):
                                oxygenobj = Lead.objects.create(
                                    needtype=need, provider=i["Provider"], contact=i["Contact"], state=state, district=district, address=i["Address"], name=i["Name"])
                                Worksheet.update_cell(
                                    int(sr_no)+1, 2, str(oxygenobj.id))
                                oxygenobj.save()
                                output_list.append(f'Record created: {i["Provider"]} : {need.type}')
                                newlyadded += 1
                            else:
                                try:
                                    oxygenobj = Lead.objects.get(id=uuid)
                                    oxygenobj.needtype = need
                                    oxygenobj.provider = i["Provider"]
                                    oxygenobj.contact = i["Contact"]
                                    oxygenobj.state = state
                                    oxygenobj.district = district
                                    oxygenobj.address = i["Address"]
                                    oxygenobj.save()
                                    updated += 1
                                    output_list.append(f"Record updated: {i['Provider']} : {need.type}")
                                except:
                                    pass
                except:
                    states = str(i["State"]).split(",")
                    for state in states:
                        if(state.strip() != ""):
                            obj = getState(state)
                            if(sr_no.strip() != ""):
                                uuid = i["UUID"]
                                if(uuid.strip() == ""):
                                    oxygenobj = Lead.objects.create(
                                        needtype=need, provider=i["Provider"], contact=i["Contact"], state=obj, address=i["Address"], name=i["Name"])
                                    Worksheet.update_cell(
                                        int(sr_no)+1, 2, str(oxygenobj.id))
                                    oxygenobj.save()
                                    output_list.append(f'Record created: {i["Provider"]} : {need.type}')
                                    newlyadded += 1
                                else:
                                    try:
                                        oxygenobj = Lead.objects.get(id=uuid)
                                        oxygenobj.needtype = need
                                        oxygenobj.provider = i["Provider"]
                                        oxygenobj.contact = i["Contact"]
                                        oxygenobj.state = obj
                                        oxygenobj.address = i["Address"]
                                        oxygenobj.save()
                                        updated += 1
                                        output_list.append(f"Record updated: {i['Provider']} : {need.type}")
                                    except:
                                        pass
                        else:
                            uuid = i["UUID"]
                            if(uuid.strip() == ""):
                                oxygenobj = Lead.objects.create(
                                    needtype=need, provider=i["Provider"], contact=i["Contact"], address=i["Address"], name=i["Name"])
                                Worksheet.update_cell(
                                    int(sr_no)+1, 2, str(oxygenobj.id))
                                oxygenobj.save()
                                output_list.append(f'Record created: {i["Provider"]} : {need.type}')
                                newlyadded += 1
                            else:
                                try:
                                    oxygenobj = Lead.objects.get(id=uuid)
                                    oxygenobj.needtype = need
                                    oxygenobj.provider = i["Provider"]
                                    oxygenobj.contact = i["Contact"]
                                    oxygenobj.address = i["Address"]
                                    oxygenobj.save()
                                    updated += 1
                                    output_list.append(f"Record updated: {i['Provider']} : {need.type}")
                                except:
                                    pass
    except Exception as e:
        print(e)
        output_list.append(e)
    print("Job done")
    output_list.append(f'"Added":{newlyadded},"Updated":{updated}')
    return HttpResponse(",".join(i for i in output_list))
