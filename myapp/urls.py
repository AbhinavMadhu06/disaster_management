from django.urls import path

from myapp import views

urlpatterns=[
    path('', views.root_redirect),  # redirect base URL to login page
    path('login/', views.login_get, name='login'),
    path('loginpost/', views.loginpost, name='loginpost'),

    #path('', views.login_get),
    #path('loginpost/', views.loginpost),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.index_page),
    path('view_camp/', views.view_camp,name='view_camp'),
    path('add_camp/', views.add_camp),
    path('camp_codinators/', views.camp_codinator,name='cordinators'),
    path('add_codinators/', views.add_codinator,name='add_coordinator'),
    path('guid_codinators/', views.guid_codinator,name='guidlines'),
    path('complaints/', views.complaint_manage, name='complaint_manage'),
    path('complaints/replay/<int:id>/', views.complaint_manage_replay, name='complaint_manage_replay'),
    path('map/', views.map),
    path('emergency_res/', views.emergency_res,name='emergency_res'),
    path('change_pass/', views.password_change),
    path('admin_password_post/', views.admin_password_post),
    path('notification/', views.notification,name='notifications'),
    path('inventories/', views.inventories),
    path('profile/', views.admin_profile),
    path('news/', views.news),
    path('admin_home/', views.index_page),
    path('add_rescue/', views.add_rescue,name='add_rescue'),


    path('ad_camp_post', views.ad_camp_post, name='ad_camp_post'),
    path('add_codinator_post', views.add_codinator_post, name='add_codinator_post'),
    path('guidlines_post',views.guid_codinator_post,name='guidlines_post'),
    path('notification_post',views.notification_post,name='notification_post'),
    path('camp/<int:id>/edit/',views.edit_camp,name='edit_camp'),
    path('coordinator/<int:id>/edit/',views.edit_coordinator,name='edit_co'),
    path('delete_coordinator/<int:id>/', views.delete_coordinator, name='delete_co'),
    path('rescue/<int:id>/edit',views.edit_rescue,name='edit_rescue'),
    path('rescue/<int:id>/delete',views.delete_rescue,name='delete_rescue'),


    path('cordinator_home/', views.cordinator_home),
     path('cordinator_profile/', views.my_coordinator_profile, name='my_coordinator_profile'),
    path('medical_support/', views.medical_support,name='medical_support'),
    path('add_medical_support/', views.medical_support_post,name='medical_support_post'),
    path('medical_support_delete/<int:id>/', views.delete_medicine_request,name='medical_support_delete'),
    path('member_register/', views.member_register,name='member_register'),
    path('add_member/', views.add_member,name='add_member'),
    path('edit_member/<int:id>', views.edit_member,name='edit_member'),
    path('delete_member/<int:id>/', views.delete_member, name='delete_member'),
    path('stock_management/', views.stock_management,name='stock_management'),
    path('add_stock/',views.stock_management_post,name='add_stock'),
    path('edit_stock/<int:id>/',views.edit_stock,name='edit_stock'),
    path('delete_stock/<int:id>/', views.delete_stock, name='delete_stock'),
    path('manage_needs/', views.manage_needs,name='manage_needs'),
    path('add_needs', views.manage_needs_post, name='add_needs'),
    path('edit_needs/<int:id>', views.edit_needs, name='edit_needs'),
    path('delete_needs/<int:id>', views.delete_needs, name='delete_needs'),
    path('view_user_report/', views.view_user_report),
    path('change_password/', views.change_password,name='co_pass_change'),
    path('changed_password/', views.coordinator_password_post,name='co_pass_changed'),
    path('news_report/', views.news_report),

]