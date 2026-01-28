from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group,User
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from myapp.models import *


def loginn(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            if user.groups.filter(name="Admin").exists():
                login(request,user)
                return redirect('/myapp/admin_homepage/')
            elif user.groups.filter(name="Hospital").exists():
                ob=hospital_table.objects.get(LOGIN__id=user.id)
                if ob.status=='accepted':
                    login(request,user)
                    return redirect('/myapp/hos_home/')
                else:
                    messages.warning(request,'NOT VERIFIED')
                    return redirect('/myapp/login')
        else:
            messages.warning(request, 'INVALID USERNAME OR PASSWORD')
            return redirect('/myapp/login')
    return render(request,'loginindex.html')



def verify_hosp(request):
    var = hospital_table.objects.all()
    return render(request,'admin/hsptl table.html',{'data':var})


def accpt_hos(request,id):
    ob=hospital_table.objects.get(id=id)
    ob.status='accepted'
    ob.save()
    return redirect('/myapp/verify_hosp/')
def rejt_hos(request,id):
    ob = hospital_table.objects.get(id=id)
    ob.status = 'rejected'
    ob.save()
    return redirect('/myapp/verify_hosp/')


def verify_ambulance(request):
    var=ambulance_table.objects.all()
    return render(request,'admin/ambu table.html',{'data':var})

def view_user(request):
    var=user_table.objects.all()
    return  render(request,'admin/view users.html',{'data':var})

def view_rating(request):
    var=rating_table.objects.all()
    return render(request,'admin/view rating.html',{'data':var})

def admin_view_complaint(request):
    var=complaint_table.objects.all()
    return render(request,'admin/view complaint.html',{'data':var})

def change_password(request):
    return render(request,'admin/chngepass.html')

def admin_change_password_post(request):
    old=request.POST['old']
    new=request.POST['new']
    f=check_password(old,request.user.password)
    if f:
        user=request.user
        user.set_password(new)
        user.save()
        messages.success(request,'password changed !!')
        return redirect('/myapp/admin_homepage/')
    else:
        messages.warning(request,'please try again')
        return redirect('/myapp/change_password/')






def admin_homepage(request):
    return render(request,'admin/admin_index1.html')

def sendReply(request,id):
    request.session['rid']=id
    return render(request,'admin/send reply.html')
def sendreply_post(request):
    reply=request.POST['reply']
    ob=complaint_table.objects.get(id=request.session['rid'])
    ob.reply=reply
    ob.save()
    return redirect('/myapp/admin_view_complaint/')




# =============================== Hospital ==========================

def hos_home(request):
    return render(request,'hospital/hospital_index.html')



def registration(request):
    return render(request,'hospital/hsptl reg.html')

def reg_post(request):
    name=request.POST['hospital_name']
    phone=request.POST['phone']
    email=request.POST['email']
    place=request.POST['place']
    post=request.POST['post']
    district=request.POST['district']
    logo=request.FILES['logo']
    username=request.POST['username']
    password=request.POST['password']
    latitude=request.POST['latitude']
    longitude=request.POST['longitude']


    fs=FileSystemStorage()
    path=fs.save(logo.name,logo)
    l=User.objects.create(username=username,password=make_password(password))

    l.groups.add(Group.objects.get(name="Hospital"))
    obj=hospital_table()
    obj.LOGIN=l
    obj.name=name
    obj.phone=phone
    obj.email=email
    obj.place=place
    obj.post=post
    obj.district=district
    obj.logo=path
    obj.latitude=latitude
    obj.longitude=longitude
    obj.status="pending"
    obj.save()
    l.save()
    return redirect('/myapp/login/')


def send_complaint(request):
    return render(request,'hospital/send ccomplaint.html')

def sndcomp_post(request):
    complaint=request.POST['complaint']
    ob=complaint_table()
    ob.LOGIN_id=request.user.id
    ob.date=datetime.now().today()
    ob.reply="pending"
    ob.complaint=complaint
    ob.save()
    return redirect('/myapp/view_complaint/')



def view_complaint(request):
    data=complaint_table.objects.filter(LOGIN_id=request.user.id)
    return render(request,'hospital/view comp hsptl.html',{'data':data})

def view_accident(request):
    var=accident_report_table.objects.all()
    return render(request,'hospital/view accdnt alert.html',{'data':var})



def add_medicalreport(request,id):
    request.session['aid']=id
    return render(request,'hospital/add medical report.html')


def addmed_post(request):
    report=request.POST['report']
    ob=medical_report_table()
    ob.date=datetime.now().today()
    ob.report=report
    ob.ACCIDENT=accident_report_table.objects.get(id=request.session['aid'])
    ob.HOSPITAL=hospital_table.objects.get(LOGIN_id=request.user.id)
    ob.save()
    return redirect('')


def view_medicalreport(request):
    var=medical_report_table.objects.all()
    return render(request,'hospital/view medical report.html',{'data':var})




def edit_medicalreport(request):
    return render(request,'hospital/edit medical report.html')
def editmed_post(request):
    report=request.POST['report']
    report = request.POST['report']
    ob = medical_report_table()
    ob.date = datetime.now().today()
    ob.report = report
    ob.ACCIDENT = accident_report_table.objects.get(id=request.session['aid'])
    ob.HOSPITAL = hospital_table.objects.get(LOGIN_id=request.user.id)
    ob.save()
    return redirect('')




########flutter


def FlutterLogin(request):
    print(request.POST)
    username=request.POST['username']
    password=request.POST['password']
    latitude=request.POST['latitude']
    longitude=request.POST['longitude']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.groups.filter(name="Ambulance").exists():
           return JsonResponse({"status":"ok","type":"Ambulance","lid":user.id})
        elif user.groups.filter(name="User").exists():
            ob=user_table.objects.get(LOGIN=user.id)
            ob.latitude=latitude
            ob.longitude=longitude
            ob.save()
            return JsonResponse({"status": "ok", "type": "User", "lid": user.id})

    return JsonResponse({"status": "na"})


def UserRegistration(request):
    name=request.POST['name']
    phone=request.POST['number']
    email=request.POST['email']
    place=request.POST['place']
    pincode=request.POST['pincode']
    district=request.POST['district']
    photo=request.FILES['photo']
    username=request.POST['username']
    password=request.POST['password']
    user=User.objects.create(username=username,password=make_password(password))
    user.save()
    user.groups.add(Group.objects.get(name='User'))
    ob=user_table()
    ob.name=name
    ob.phone=phone
    ob.email=email
    ob.place=place
    ob.pincode=pincode
    ob.district=district
    ob.latitude='0'
    ob.longitude='0'
    ob.photo=photo
    ob.LOGIN=user
    ob.save()
    return JsonResponse({'status':'ok'})

def ambulanceregistration(request):
    registration=request.POST['reg']
    drivername=request.POST['name']
    phone = request.POST['number']
    email = request.POST['email']
    photo = request.FILES['photo']
    # status=request.POST['status']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    username = request.POST['username']
    password = request.POST['password']
    user = User.object.create(username=username, password=make_password(password))
    user.save()
    user.groups.add(Group.objects.get(name='Ambulance'))
    ob=ambulance_table()
    ob.registration_no=registration
    ob.drivers_name=drivername
    ob.phone=phone
    ob.email=email
    ob.latitude=latitude
    ob.longitude=longitude
    ob.status="pending"
    ob.LOGIN=User
    ob.rc=photo
    ob.save()
    return JsonResponse ({'status':'ok'})

def ambulance_view_profile(request):
    lid=request.POST['lid']
    ob=ambulance_table.objects.get(LOGIN__id=lid)
    dic={"reg_no":ob.registration_no,"name":ob.drivers_name
        ,"rc":ob.rc.url,"phone":ob.phone,"email":ob.email,
         "status":ob.status}
    return JsonResponse ({'status':'ok',"data":dic})

def ambulance_edit_profile(request):
    lid=request.POST['lid']
    return JsonResponse ({'status':'ok'})


def ambulance_send_complaint(request):
    return JsonResponse ({'status':'ok'})


def ambulance_view_complaint(request):
    return JsonResponse ({'status':'ok'})

def ambulance_view_nearest_hospital(request):
    return JsonResponse ({'status':'ok'})

def ambulance_view_notification(request):
    return JsonResponse ({'status':'ok'})


def userview_profile(request):
    lid=request.POST['lid']
    var=user_table.objects.get(LOGIN=lid)
    image_url = request.build_absolute_uri(var.photo)
    print(var.photo.url)
    return JsonResponse({'status':"ok","name":var.name,"phone":str(var.phone),"email":var.email,"place":var.place,"pincode":str(var.pincode),"district":var.district,"photo":str(var.photo.url)})

def User_updateprofile(request):
    print(request.FILES,"**********************")
    lid=request.POST['lid']
    name=request.POST['name']
    phone=request.POST['phone']
    email=request.POST['email']
    place=request.POST['place']
    pincode=request.POST['pincode']
    district=request.POST['district']

    ob=user_table.objects.get(LOGIN=lid)
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        ob.photo = photo
    ob.name=name
    ob.phone=phone
    ob.email=email
    ob.place=place
    ob.pincode=pincode
    ob.district=district
    ob.save()
    return JsonResponse({'status':'ok'})







def sendcomplaintuser(request):
    comp = request.POST['complaint']
    lid = request.POST['lid']
    lob = complaint_table()
    lob.LOGIN = User.objects.get(id=lid)
    lob.complaint = comp
    lob.reply = 'pending'
    lob.date = datetime.today()
    lob.save()
    return JsonResponse({'task': 'ok'})


def viewcomplaintuser(request):
    lid=request.POST['lid']
    ob=complaint_table.objects.filter(LOGIN__id=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'complaint':i.complaint,
              'reply':i.reply,
              'date':str(i.date)}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})

def view_nearest_hospital(request):
    lid=request.POST['lid']
    ob=hospital_table.objects.all
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'id':i.id,
              'name':i.name,
              'phone':str(i.phone),
              'place':i.place,
              'post':str(i.post),
              'district':i.district,
              'logo':i.logo,
              'email':i.email,
              'status':i.status,
              'longitude':str(i.longitude),
              'latitude':str(i.latitude),
              }


        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})
