from django.urls import path

from myapp import views

urlpatterns = [

    path('logout_get/',views.logout_get),
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
    path('add_medicalreport/', views.add_medicalreport),
    path('addmed_post/', views.addmed_post),
    path('view_medicalreport/<id>/', views.view_medicalreport),
    path('edit_medicalreport/<id>', views.edit_medicalreport),

    path('UserRegistration/', views.UserRegistration),
    path('FlutterLogin/', views.FlutterLogin),
    path('ambulance_view_profile/', views.ambulance_view_profile),
    path('ambulanceregistration/', views.ambulanceregistration),
    path('ambulance_edit_profile/', views.ambulance_edit_profile),
    path('ambulance_send_complaint/', views.ambulance_send_complaint),
    path('ambulance_view_complaint/', views.ambulance_view_complaint),
    path('ambulance_view_nearest_hospital/', views.ambulance_view_nearest_hospital),
    path('ambulance_view_notification/', views.ambulance_view_near_notification),
    path('userview_profile/', views.userview_profile),
    path('User_updateprofile/', views.User_updateprofile),
    path('viewcomplaintuser/', views.viewcomplaintuser),
    path('sendcomplaintuser/', views.sendcomplaintuser),
    path('user_view_near_notification/', views.user_view_near_notification),
    path('user_view_near_ambulance/', views.user_view_near_ambulance),
    path('send_feedback/', views.sendFeedback),
    path('ambulance_view_near_accidents/', views.ambulance_view_near_accidents),
    path('ambulance_update_accident_status/', views.update_accident_status),
    path('ambulance_view_accident_notification/', views.ambulance_view_accident_notification),

    path('hospital_view_profile/', views.hospital_view_profile, name='hospital_view_profile'),
    path('hospital_edit_profile/', views.hospital_edit_profile_get, name='hospital_edit_profile_get'),
    path('hospital_edit_profile_post/', views.hospital_edit_profile_post, name='hospital_edit_profile_post'),
    path('user_view_near_accidents/', views.user_view_near_accidents, name='user_view_near_accidents'),

    path('accident_detection/', views.accident_detection, name='accident_detection'),
    path('online_update_status/', views.online_update_status, name='online_update_status'),
    path('offline_update_status/', views.offline_update_status, name='offline_update_status'),
    path('update_location/', views.update_location, name='update_location'),



#     chat web

    path('accpt_amb/<id>', views.accpt_amb, name='accpt_amb'),
    path('rejt_amb/<id>', views.rejt_amb, name='rejt_amb'),



    path('chat1/<id>', views.chat1, name='chat1'),
    path('chat_view/', views.chat_view, name='chat_view'),
    path('chat_send_web/<msg>', views.chat_send_web, name='chat_send_web'),

#     flutter chat
    path('chat_send/', views.chat_send, name='chat_send'),
    path('chat_view_and/', views.chat_view_and, name='chat_view_and'),

    path('user_change_password_post/', views.user_change_password_post, name='user_change_password_post'),
    path('amb_change_password_post/', views.amb_change_password_post, name='amb_change_password_post'),

    path('user_Forgot_password/', views.user_Forgot_password, name='user_Forgot_password'),

]
