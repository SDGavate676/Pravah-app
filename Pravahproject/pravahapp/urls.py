from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # path('empregistration/', views.empregistration, name='empregistration'),
    # path('emplogin/', views.emplogin, name='emplogin'),
    # path('emplogout/', views.emplogout, name='emplogout'),
    path('emp_profile/', views.emp_profile, name='emp_profile'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('profile_success/', views.profile_success, name='profile_success'), 
    path('profile_successcandidate/', views.profile_successcandidate, name='profile_successcandidate'), 
    path('educationdetail/', views.educationdetail, name='educationdetail'),
    path('submitcv/', views.submitcv, name='submitcv'),
    path('', views.index, name='index'),
   
    path('about/', views.about, name='about'),
    path('ourservices/', views.ourservices, name='ourservices'),
    path('service/', views.service, name='service'),
    path('features/', views.features, name='features'),
    path('jobpostings/', views.jobpostings, name='jobpostings'),
    path('contact/', views.contact, name='contact'), 
    
    path('joblist/', views.joblist, name='joblist'),
    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('success_page/', views.success_page, name='success_page'),



]