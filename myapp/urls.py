from django.urls import path

from myapp import views

urlpatterns = [
    path('login/',views.loginn),
    path('verify_hosp/',views.verify_hosp),
    path('verify_ambulance/',views.verify_ambulance),
    path('view_user/',views.view_user),
    path('view_rating/',views.view_rating),
    path('admin_view_complaint/',views.admin_view_complaint),
    path('change_password/',views.change_password),
    path('admin_change_password_post/',views.admin_change_password_post),
    path('admin_homepage/',views.admin_homepage),
    path('sendReply/<id>/',views.sendReply),
    path('accpt_hos/<id>/',views.accpt_hos),
    path('rejt_hos/<id>/',views.rejt_hos),
    path('sendreply_post/',views.sendreply_post),



    path('hos_home/',views.hos_home),
    path('registration/',views.registration),
    path('reg_post/',views.reg_post),
    path('send_complaint/',views.send_complaint),
    path('sndcomp_post/',views.sndcomp_post),
    path('view_complaint/',views.view_complaint),
    path('view_accident/',views.view_accident),
    path('add_medicalreport/<id>/', views.add_medicalreport),
    path('view_medicalreport/', views.view_medicalreport),
    path('edit_medicalreport/', views.edit_medicalreport),



    path('UserRegistration/', views.UserRegistration),
    path('FlutterLogin/', views.FlutterLogin),
    path('ambulance_view_profile/', views.ambulance_view_profile),
    path('ambulanceregistration/', views.ambulanceregistration),
    path('ambulance_edit_profile/', views.ambulance_edit_profile),
    path('ambulance_send_complaint/', views.ambulance_send_complaint),
    path('ambulance_view_complaint/', views.ambulance_view_complaint),
    path('ambulance_view_nearest_hospital/', views.ambulance_view_nearest_hospital),
    path('ambulance_view_notification/', views.ambulance_view_notification),
    path('userview_profile/', views.userview_profile),
    path('User_updateprofile/', views.User_updateprofile),
    path('viewcomplaintuser/', views.viewcomplaintuser),
    path('sendcomplaintuser/', views.sendcomplaintuser),


]
