from django.http.response import Http404
from django.shortcuts import HttpResponse
from .models import NeedType, Lead, State, District
from covid.renderer import renderView
import gspread
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
    print(Ratios)
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
        itemFrom = int(request.POST['from'])-1
        itemTo = int(request.POST['till'])
        if itemTo < 10:
            itemTo = 10
    except:
        itemFrom = 0
        itemTo = 10
    try:
        needobj = NeedType.objects.get(id=need)
        states = []
        districts = []
        resources = []
        try:
            statename = str(request.GET['state'])
            state = State.objects.get(name=statename)
            districts = District.objects.filter(state=state)
        except:
            states = State.objects.all()
            state = None

        district = None
        if state:
            try:
                distname = str(request.GET['district'])
                district = District.objects.get(name=distname, state=state)
            except:
                district = None

        if district:
            resources = Lead.objects.filter(needtype=needobj,state=state,district=district)[itemFrom:itemTo]
            totalleads = Lead.objects.filter(needtype=needobj,state=state,district=district).count()
        elif state:
            resources = Lead.objects.filter(needtype=needobj,state=state)[itemFrom:itemTo]
            totalleads = Lead.objects.filter(needtype=needobj,state=state).count()
        else:
            resources = Lead.objects.filter(needtype=needobj)[itemFrom:itemTo]
            totalleads = Lead.objects.filter(needtype=needobj).count()
        
        if itemTo > totalleads:
            itemTo = totalleads
        data = {
            'leads': resources,
            'need': needobj,
            "states": states,
            "districts": districts,
            "state": state,
            "district": district,
            "from":itemFrom+1,
            "till":itemTo,
            "totalleads": totalleads
        }
        return renderView(request, 'leads.html', data)
    except:
        raise Http404()

def addwithDistrict(sr_no,district,state,need,lead):
    if(sr_no.strip() != ""):
        uuid = lead["UUID"]
        if(uuid.strip() == ""):
            oxygenobj = Lead.objects.create(
                needtype=need, provider=lead["Provider"], contact=lead["Contact"], state=state, district=district, address=lead["Address"], name=lead["Name"])
            oxygenobj.save()
            return oxygenobj,True
        else:
            try:
                oxygenobj = Lead.objects.get(id=uuid)
                oxygenobj.needtype = need
                oxygenobj.provider = lead["Provider"]
                oxygenobj.contact = lead["Contact"]
                oxygenobj.state = state
                oxygenobj.district = district
                oxygenobj.address = lead["Address"]
                oxygenobj.save()
                return oxygenobj,False
            except:
                pass


def addwithoutDistrict(sr_no,state,need,lead):
    obj = getState(state)
    if(obj!=False):
        state = obj
        if(sr_no.strip() != ""):
            uuid = lead["UUID"]
            if(uuid.strip() == ""):
                oxygenobj = Lead.objects.create(
                    needtype=need, provider=lead["Provider"], contact=lead["Contact"], state=state, address=lead["Address"], name=lead["Name"])
                oxygenobj.save()
                return oxygenobj,True
            else:
                try:
                    oxygenobj = Lead.objects.get(id=uuid)
                    oxygenobj.needtype = need
                    oxygenobj.provider = lead["Provider"]
                    oxygenobj.contact = lead["Contact"]
                    oxygenobj.state = state
                    oxygenobj.address = lead["Address"]
                    oxygenobj.save()
                    return oxygenobj,False
                except:
                    pass


def delRajat():
    objs = Lead.objects.filter(provider="Rajat Air Products")
    for i in objs:
        i.delete()


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
                output_list.append(f"Worksheet found: {need.type}")
            except:
                output_list.append(f"Worksheet not found: {need.type}")
                continue
            res = Worksheet.get_all_records()
            count = 0
            for i in res:
                if(count==7):
                    break
                count+=1
                sr_no = str(i["Sr. No."])
                try:
                    if(i["District"].strip()==""):
                        raise Exception
                    districts = str(i["District"]).split(",")
                    for dis in districts:
                        obj = getDistrict(dis)
                        if(obj == False):
                            newobj,is_added = addwithoutDistrict(sr_no,i["State"],need,i)
                            Worksheet.update_cell(int(sr_no)+1, 2, str(newobj.id))
                            if(is_added):
                                output_list.append(f'Record created: {newobj.provider} : {need.type}')
                                newlyadded += 1
                            else:
                                output_list.append(f"Record updated: {newobj.provider} : {need.type}")
                                updated+=1
                        else:
                            district, state = obj, obj.state
                            newobj,is_added = addwithDistrict(sr_no,district,state,need,i)
                            Worksheet.update_cell(int(sr_no)+1, 2, str(newobj.id))
                            if(is_added):
                                output_list.append(f'Record created: {newobj.provider} : {need.type}')
                                newlyadded += 1
                            else:
                                output_list.append(f"Record updated: {newobj.provider} : {need.type}")
                                updated+=1
                except Exception as e:
                    print(e)
                    states = str(i["State"]).split(",")
                    for sts in states:
                        newobj,is_added = addwithoutDistrict(sr_no,sts,need,i)
                        Worksheet.update_cell(int(sr_no)+1, 2, str(newobj.id))
                        if(is_added):
                            output_list.append(f'Record created: {newobj.provider} : {need.type}')
                            newlyadded += 1
                        else:
                            output_list.append(f"Record updated: {newobj.provider} : {need.type}")
                            updated+=1

                        
    except Exception as e:
        print(e)
        output_list.append("Some error occured")

    return HttpResponse(",".join(i for i in output_list))
