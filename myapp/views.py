from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group,User
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from myapp.models import *


def loginn(request):
    # us=User.objects.get(id=7)
    # us.set_password('mims')
    # us.save()
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
    return render(request,'Hospital/hospital_index.html')



def registration(request):
    return render(request,'Hospital/hsptl reg.html')

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
    return render(request,'Hospital/send ccomplaint.html')

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
    return render(request,'Hospital/view comp hsptl.html',{'data':data})

def view_accident(request):
    var=accident_report_table.objects.filter(HOSPITAL__LOGIN_id=request.user.id)
    return render(request,'Hospital/view accdnt alert.html',{'data':var})



def add_medicalreport(request):
    return render(request,'Hospital/add medical report.html')


def addmed_post(request):
    report=request.POST['report']
    ob=medical_report_table()
    ob.date=datetime.now().today()
    ob.report=report
    ob.ACCIDENT=accident_report_table.objects.get(id=request.session['aid'])
    ob.HOSPITAL=hospital_table.objects.get(LOGIN_id=request.user.id)
    ob.save()
    return redirect(f'/myapp/view_medicalreport/{request.session["aid"]}/')


def view_medicalreport(request,id):
    request.session['aid']=id
    var=medical_report_table.objects.filter(ACCIDENT_id=id)
    return render(request,'Hospital/view medical report.html',{'data':var})




def edit_medicalreport(request):
    return render(request,'Hospital/edit medical report.html')
def editmed_post(request):
    report = request.POST['report']
    ob = medical_report_table()
    ob.date = datetime.now().today()
    ob.report = report
    ob.ACCIDENT = accident_report_table.objects.get(id=request.session['aid'])
    ob.HOSPITAL = hospital_table.objects.get(LOGIN_id=request.user.id)
    ob.save()
    return redirect('')


@login_required
def hospital_view_profile(request):
    """View hospital profile"""
    try:
        # Get the hospital profile for the logged-in user
        hospital = hospital_table.objects.get(LOGIN=request.user)

        context = {
            'hospital': hospital
        }
        return render(request, 'Hospital/hospital_profile.html', context)

    except hospital_table.DoesNotExist:
        messages.error(request, "Hospital profile not found")
        return redirect('login')  # Redirect to login or appropriate page


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import hospital_table
import os
from django.conf import settings


@login_required
def hospital_edit_profile_get(request):
    """Display edit profile form"""
    try:
        hospital = hospital_table.objects.get(LOGIN=request.user)

        context = {
            'hospital': hospital
        }
        return render(request, 'Hospital/edit_profile.html', context)

    except hospital_table.DoesNotExist:
        messages.error(request, "Hospital profile not found")
        return redirect('login')


@login_required
def hospital_edit_profile_post(request):
    """Handle edit profile form submission"""
    if request.method == 'POST':
        try:
            hospital = hospital_table.objects.get(LOGIN=request.user)

            # Update hospital details
            hospital.name = request.POST.get('hospital_name')
            hospital.phone = request.POST.get('phone')
            hospital.email = request.POST.get('email')
            hospital.place = request.POST.get('place')
            hospital.post = request.POST.get('post')
            hospital.district = request.POST.get('district')
            hospital.latitude = request.POST.get('latitude')
            hospital.longitude = request.POST.get('longitude')

            # Handle logo upload if a new file is provided
            if 'logo' in request.FILES:
                # Delete old logo if exists
                if hospital.logo and os.path.exists(os.path.join(settings.MEDIA_ROOT, hospital.logo)):
                    os.remove(os.path.join(settings.MEDIA_ROOT, hospital.logo))

                # Save new logo
                logo_file = request.FILES['logo']
                logo_path = f'hospital_logos/{hospital.LOGIN.username}_{logo_file.name}'

                # Save file
                from django.core.files.storage import FileSystemStorage
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'hospital_logos'))
                filename = fs.save(f'{hospital.LOGIN.username}_{logo_file.name}', logo_file)
                hospital.logo = f'hospital_logos/{filename}'

            hospital.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('hospital_view_profile')

        except hospital_table.DoesNotExist:
            messages.error(request, "Hospital profile not found")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error updating profile: {str(e)}")
            return redirect('hospital_edit_profile_get')

    return redirect('hospital_edit_profile_get')









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
            ob = ambulance_table.objects.get(LOGIN=user.id)
            ob.latitude = latitude
            ob.longitude = longitude
            ob.save()

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
    phone = request.POST['phone']
    email = request.POST['email']

    photo = request.FILES['photo']
    # status=request.POST['status']
    # latitude = request.POST['latitude']
    # longitude = request.POST['longitude']
    username = request.POST['username']
    password = request.POST['password']


    user = User.objects.create(username=username, password=make_password(password))
    user.save()
    user.groups.add(Group.objects.get(name='Ambulance'))
    ob=ambulance_table()
    ob.registration_no=registration
    ob.drivers_name=drivername
    ob.phone=phone
    ob.email=email
    ob.latitude=0
    ob.longitude=0
    ob.status="pending"
    ob.LOGIN=user
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
    registration = request.POST['reg']
    drivername = request.POST['name']
    phone = request.POST['number']
    email = request.POST['email']
    photo = request.FILES.get('photo')
    # status=request.POST['status']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    # username = request.POST['username']
    # password = request.POST['password']
    # user = User.object.create(username=username, password=make_password(password))
    # user.save()
    # user.groups.add(Group.objects.get(name='Ambulance'))
    ob = ambulance_table.objects.get(LOGIN_id=lid)
    ob.registration_no = registration
    ob.drivers_name = drivername
    ob.phone = phone
    ob.email = email
    ob.latitude = latitude
    ob.longitude = longitude
    ob.status = "pending"
    ob.LOGIN = User
    if photo:
        ob.rc = photo
    ob.save()
    return JsonResponse ({'status':'ok'})


def ambulance_send_complaint(request):
    complaint = request.POST['complaint']
    lid = request.POST['lid']
    ob = complaint_table()
    ob.LOGIN_id = lid
    ob.date = datetime.now().today()
    ob.reply = "pending"
    ob.complaint = complaint
    ob.save()
    return JsonResponse ({'status':'ok'})


def ambulance_view_complaint(request):
    lid =request.POST['lid']
    data=complaint_table.objects.filter(LOGIN_id=lid)
    l=[]
    for i in data:
       l.append({
           "id":i.id,
           "complaint":i.complaint,
           "date":i.date,
           "reply":i.reply,
       })

    return JsonResponse ({'status':'ok','data':l})

# def ambulance_view_nearest_hospital(request):
#     lid = request.POST['lid']
#     data = hospital_table.objects.all()
#     l = []
#     for i in data:
#         l.append({
#             "id": i.id,
#             "name": i.name,
#             "phone": i.phone,
#             "email": i.email,
#             "place": i.place,
#             "post": i.post,
#             "district": i.district,
#             "logo": i.logo,
#             "status": i.status,
#             "latitude": i.latitude,
#             "longitude": i.longitude,
#         })
#
#     return JsonResponse ({'status':'ok'})


from django.http import JsonResponse
from math import radians, cos, sin, asin, sqrt
from .models import hospital_table

# Haversine formula to calculate distance in km
def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def ambulance_view_nearest_hospital(request):
    # lid = request.POST['lid']
    am_lat = float(request.POST['latitude'])
    am_lon = float(request.POST['longitude'])

    data = hospital_table.objects.all()
    nearby_hospitals = []
    for i in data:
        distance = haversine(am_lat, am_lon, i.latitude, i.longitude)
        print(distance,"distance")
        if distance <= 20:  # filter within 10 km
            nearby_hospitals.append({
                "id": i.id,
                "name": i.name,
                "phone": i.phone,
                "email": i.email,
                "place": i.place,
                "post": i.post,
                "district": i.district,
                "logo": i.logo,
                "status": i.status,
                "latitude": i.latitude,
                "longitude": i.longitude,
                "distance": round(distance, 2)
            })
    return JsonResponse({'status': 'ok', 'data': nearby_hospitals})


def ambulance_view_near_notification(request):
    am_lat = float(request.POST['latitude'])
    am_lon = float(request.POST['longitude'])
    data = notification_table.objects.all()
    l = []
    for i in data:
        distance = haversine(am_lat, am_lon, i.latitude, i.longitude)
        print(distance, "distance")
        if distance <= 20:  # filte
            l.append({
                "id": i.id,
                "latitude": i.latitude,
                "longitude": i.longitude,
                "date": i.date,
                "photo": i.photo,
                "u_name": i.USER.name,
                "u_phone": i.USER.phone,
                "u_latitude": i.USER.latitude,
                "u_longitude": i.USER.latitude,
            })

    return JsonResponse ({'status':'ok'})




# ==================user===================

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
    ob=hospital_table.objects.all()
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

# def user_view_near_notification(request):
#     am_lat = float(request.POST['latitude'])
#     am_lon = float(request.POST['longitude'])
#     data = notification_table.objects.all()
#     l = []
#     for i in data:
#         distance = haversine(am_lat, am_lon, i.latitude, i.longitude)
#         print(distance, "distance")
#         if distance <= 20:  # filte
#             l.append({
#                 "id": i.id,
#                 "latitude": i.latitude,
#                 "longitude": i.longitude,
#                 "date": i.date,
#                 "photo": i.photo,
#                 "u_name": i.USER.name,
#                 "u_phone": i.USER.phone,
#                 "u_latitude": i.USER.latitude,
#                 "u_longitude": i.USER.latitude,
#             })
#
#     return JsonResponse ({'status':'ok'})


def user_view_near_notification(request):
    am_lat = float(request.POST['latitude'])
    am_lon = float(request.POST['longitude'])
    data = notification_table.objects.all()
    l = []
    for i in data:
        distance = haversine(am_lat, am_lon, i.latitude, i.longitude)
        if distance <= 20:
            l.append({
                "id": i.id,
                "latitude": i.latitude,
                "longitude": i.longitude,
                "date": i.date,
                "photo": str(i.photo.url) if i.photo else "",
                "u_name": i.USER.name,
                "u_phone": i.USER.phone,
                "u_latitude": i.USER.latitude,
                "u_longitude": i.USER.longitude,
                "distance": round(distance, 2),
            })
    return JsonResponse({'status': 'ok', 'data': l})

def user_view_near_ambulance(request):
    am_lat = float(request.POST['latitude'])
    am_lon = float(request.POST['longitude'])
    data = ambulance_table.objects.all()
    l = []
    for i in data:
        distance = haversine(am_lat, am_lon, i.latitude, i.longitude)
        print(distance,"ddddddd")
        if distance <= 20:  # within 20 km radius
            l.append({
                "id": i.id,
                "registration_no": i.registration_no,
                "drivers_name": i.drivers_name,
                "phone": i.phone,
                "email": i.email,
                "latitude": i.latitude,
                "longitude": i.longitude,
                "status": i.status,
                "rc": str(i.rc.url) if i.rc else "",
                "login_user": i.LOGIN.username,  # from User model
                "distance": round(distance, 2),
            })
    return JsonResponse({'status': 'ok', 'data': l})


def sendFeedback(request):
    comp = request.POST['comments']
    lid = request.POST['lid']
    rating = request.POST['rating']

    lob = rating_table()
    lob.USER = user_table.objects.get(LOGIN_id=lid)
    lob.review = comp
    lob.rating = rating
    lob.date = datetime.today()
    lob.save()
    return JsonResponse({'status': 'ok'})




# accident detection


def accident_detection(request):
    userid = request.POST.get('uid')
    image = request.FILES.get('image')

    fs=FileSystemStorage()
    path=fs.save(image.name,image)

    user=user_table.objects.get(id=userid)
    us_lat=user.latitude
    us_lon=user.longitude

    amb = ambulance_table.objects.all()
    hosp = hospital_table.objects.all()



    lob = accident_report_table()
    lob.USER = user
    lob.latitude = user.latitude
    lob.longitude = user.longitude
    lob.photo = path
    lob.date = datetime.today()

    for i in amb:
        distance = haversine(us_lat, us_lon, i.latitude, i.longitude)
        if distance <= 20:
            lob.AMBULANCE = i
    for i in hosp:
        distance = haversine(us_lat, us_lon, i.latitude, i.longitude)
        if distance <= 20:
            lob.HOSPITAL = i


    lob.status="pending"
    lob.save()
    return JsonResponse({'status': 'ok'})

