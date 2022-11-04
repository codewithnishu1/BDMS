from itertools import count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from Bloodmanager.models import Blood_request
from patient.models import Patient

def patient_signup(request):
    if request.method == "POST":
        """retrieve patient inputs"""
        name = request.POST.get('patient-name')
        eml = request.POST.get('patient-email')
        psw = request.POST.get('patient-password')
        age = request.POST.get('patient-age')
        state = request.POST.get('patient-state')
        district = request.POST.get('patient-district')
        mob = request.POST.get('patient-mob')
        bgroup = request.POST.get('patient-bgroup')
        try:
            obj = Patient.objects.get(email=eml)
        except Patient.DoesNotExist:
            # return HttpResponse('No admin profile found')
            obj = Patient()  # it is object of patient class
            obj.name = name
            obj.email = eml
            obj.password = psw
            obj.Bgroup = bgroup
            obj.age = age
            obj.mobile_no = mob
            obj.state = state
            obj.district = district

        obj.save()
        # return JsonResponse(obj, safe=False)  # actually here is patient-login.html
        return HttpResponse('patient-login.html')
    return HttpResponse('Please try again')


def patient_login(request):
    if request.method == "POST":
        """retrive admin inputs"""
        el = request.POST.get('patient-email')
        psw = request.POST.get('patient-password')
        print(el, psw)
        try:
            obj = Patient.objects.get(email=el)
        except Patient.DoesNotExist:
            return HttpResponse('No patient profile found')
        if obj.password != psw:
            return HttpResponse('incorrect password')
        # return redirect('patient-dashboard/')
        return HttpResponse('Login Successful')

def blood_request(request):
    if request.method == "POST":
        """retrieve patient inputs"""
        name = request.POST.get('patient-name')
        eml = request.POST.get('patient-email')
        bgroup = request.POST.get('patient-bgroup')
        # status = request.POST.get('patient-status')
        unit = request.POST.get('patient-unit')
        obj = Blood_request() # it is object of Blood_request class
        obj.name = name
        obj.email = eml
        # obj.status = status
        obj.Bgroup = bgroup
        obj.units = unit
        obj.save()
        l = []
        for i in Blood_request.ojects.filter(email=eml):
            dict = {}
            dict['units'] = i.units
            dict['patient_id'] = i.id
            dict["patient_name"] = i.name
            dict["bgroup"] = i.Bgroup
            dict["status"] = i.status
            l.append(dict)
        d = {'patient': l}
        return JsonResponse(d)
        # print(name,eml,bgroup,unit)
        # return HttpResponse('Successful Request')
    # return HttpResponse('Try-again')

def request_history(request,eml):
    # eml = request.POST.get('email')
    # obj = Blood_request.objects.filter(email=eml)
    l = []
    for i in Blood_request.objects.filter(email=eml):
        dict = {}
        dict['patient_id'] = i.id
        dict["patient_name"] = i.name
        dict["bgroup"] = i.Bgroup
        dict['units'] = i.units
        dict["status"] = i.status
        l.append(dict)
    d = {'patient': l}
    return JsonResponse(d)

def patient_dashBoard(request,eml):
    obj = Blood_request.objects.filter(email=eml)
    count = 0
    approved = 0
    rejected = 0
    pending = 0
    for i in obj:
        count += 1
    for j in obj:
        if j.status == 'approved':
            approved += 1
        elif j.status == 'rejected':
            rejected += 1
        else:
            pending += 1
    return JsonResponse({'dashboard': [{'Count': count}, {'pending': pending}, {'Approved': approved},
                                       {'Rejected': rejected}]})